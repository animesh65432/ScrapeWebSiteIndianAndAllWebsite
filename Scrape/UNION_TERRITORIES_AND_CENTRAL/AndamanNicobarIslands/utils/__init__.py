from config.create_driver import create_driver
from utils.load_with_retry import load_with_retry
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import urllib.parse
from  config.safe_quit import safe_quit
import asyncio


async def scrape_website(url: str):
    driver = None

    try:

        driver = await create_driver()

        if not driver:
            print(f"[scrape_website] Failed to create driver for {url}")
            return []

        if not await load_with_retry(driver, url,html_element="table", retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []

       
        loop = asyncio.get_event_loop()

        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)

        soup = BeautifulSoup(html, 'html.parser')

        driver = None

        
        table = soup.find("table")

        if not table:
            print("Table not found")
            return []

        tbody = table.find("tbody")

        if not tbody:
            print("Table body not found")
            return []

        rows = tbody.find_all("tr")

    

        today = datetime.now().strftime("%d-%m-%Y")
        announcements = []

        for row in rows:
            try:
                cells = row.find_all("td")
                if len(cells) >= 4:

                    # title
                    subject_span = cells[1].find("span", class_="bt-content")
                    title = subject_span.text.strip() if subject_span else ""

                    # date
                    date_span = cells[2].find("span", class_="bt-content")
                    upload_date = date_span.text.strip() if date_span else ""

                    if upload_date != today:
                        continue

                    # pdf link
                    pdf_link = ""
                    download_span = cells[3].find("span", class_="bt-content")
                    if download_span:
                        pdf_link_tag = download_span.find("a", href=True)
                        if pdf_link_tag:
                            pdf_link = pdf_link_tag.get("href", "")
                            if pdf_link and not pdf_link.startswith("http"):
                                pdf_link = urljoin(url, pdf_link)

                            pdf_link = urllib.parse.quote(pdf_link, safe=':/')

                    announcements.append({
                        "title": title,
                        "pdf_link": pdf_link,
                        "state": "AndamanNicobarIslands",
                    })

            except:
                continue

        return announcements

    except Exception as e:
        print("scrape_website error:", e)
        await safe_quit(driver=driver)
        driver = None
        return []
