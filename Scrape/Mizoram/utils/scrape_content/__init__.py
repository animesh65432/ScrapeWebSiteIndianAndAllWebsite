from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def scrape_content(url: str):
    driver = None
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

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
            return "Content not found"

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # try to find any container
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
        return f"An error occurred in scrape_content: {e}"

    finally:
        if driver:
            driver.quit()
