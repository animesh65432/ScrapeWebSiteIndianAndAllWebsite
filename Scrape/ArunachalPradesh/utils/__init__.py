from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re

def scrape_website(url: str) -> dict:
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # run without GUI
        chrome_options.add_argument("--ignore-certificate-errors")  # ignore SSL issues
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(options=chrome_options)

        # Open URL
        driver.get(url)
        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, "html.parser")

        print(soup)

        return []

    except Exception as e:
        return e
