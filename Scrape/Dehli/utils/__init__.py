from selenium import webdriver
from config.chromeOptions import Get_Chrome_Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_website(url: str):
    chrome_options = Get_Chrome_Options()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # Wait for elements to load dynamically
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".tab-date"))
    )

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")
    results = []

    for li in soup.select("li"):
        # Title
        title_el = li.select_one(".tab-title")
        if title_el:
            for child in title_el.find_all():
                child.decompose()
            title = title_el.get_text(strip=True)
        else:
            title = ""

        # Link
        link_el = li.select_one("a.tab-view")
        link = urljoin("https://delhi.gov.in", link_el.get("href")) if link_el else ""

        if title and link:
            results.append({
                "title": title,
                "link": link,
            })

    return results
