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

        # CSS selector for ANY valid content container
        html_element = (
            "div.post-content, "
            "div.content-body, "
            "div.full-post-content, "
            "div.entry-content"
        )

        if not await load_with_retry(driver, url, html_element, retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            driver = None
            return "Page failed to load"

        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        soup = BeautifulSoup(html, "html.parser")

        await safe_quit(driver=driver)
        driver = None

        # Find actual content container
        content_div = (
            soup.find("div", class_="post-content") or
            soup.find("div", class_="content-body") or
            soup.find("div", class_="full-post-content") or
            soup.find("div", class_="entry-content")
        )

        if not content_div:
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
