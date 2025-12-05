from config.create_driver import create_driver
from utils.load_with_retry import load_with_retry
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config.safe_quit import safe_quit
from bs4 import BeautifulSoup
import asyncio

async def scrape_content(url: str):

    driver = None

    try:
        driver = await create_driver()
        
        if not await  load_with_retry(driver, url, retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            driver = None
            return "Page failed to load"

        # WAIT for any possible content containers
        possible_selectors = [
            (By.CLASS_NAME, "post-content"),
            (By.CLASS_NAME, "content-body"),
            (By.CLASS_NAME, "full-post-content"),
            (By.CLASS_NAME, "entry-content")
        ]

        element = None
        wait = WebDriverWait(driver, 10)

        for selector in possible_selectors:
            try:
                element = wait.until(EC.presence_of_element_located(selector))
                break
            except:
                continue

        if not element:
            safe_quit(driver=driver)
            driver = None
            return "Content not found"
        
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        soup = BeautifulSoup(html, "html.parser")

        await safe_quit(driver=driver)
        driver = None

        # try to find any container
        content_div = (
            soup.find("div", class_="post-content") or
            soup.find("div", class_="content-body") or
            soup.find("div", class_="full-post-content") or
            soup.find("div", class_="entry-content")
        )

        if not content_div:
            safe_quit(driver=driver)
            return "Content not found"

        markdown = ""
        paragraphs = content_div.find_all("p")


        for p in paragraphs:
            text = p.get_text(strip=True)
            if text:
                markdown += text + "\n\n"

        return markdown.strip()

    except Exception as e:
        await safe_quit(driver=driver)
        return f"An error occurred in scrape_content: {e}"

   
