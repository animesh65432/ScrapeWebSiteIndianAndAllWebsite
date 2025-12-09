from datetime import datetime
from config.create_driver import create_driver
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from utils.load_with_retry import load_with_retry
from  config.safe_quit import safe_quit
import asyncio

async def scrape_website(url: str):
    driver = None
    try:
        driver = await create_driver()

        if not await load_with_retry(driver, url, html_element="table",part="south_india",retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []
        
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None

        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", {"class": "table-striped table-bordered table"})
        
        if not table:
            print("Table not found!")
            return []

        notices = []

        rows = table.find("tbody").find_all("tr")

        for row in rows[1:]:     
            cells = row.find_all("td")
            date_str = cells[2].get_text(strip=True)
            subject = cells[3].get_text(strip=True)

            
            try:
                scraped_date = datetime.strptime(date_str, "%d-%m-%Y").date()
            except:
                continue  # skip invalid dates
            
            
            if scraped_date != datetime.today().date():
                continue   # skip anything not today

            view_link = cells[5].find("a")
            view_url = None

            if view_link:
                href = view_link.get("href")
                if href:
                    view_url = urljoin("https://egovernance.karnataka.gov.in/", href)

            if view_url:
                notices.append({
                    "date": date_str,
                    "title": subject,
                    "pdf_link": view_url
                })

        return notices

    except Exception as e:
        print("Scraping Error:", str(e))

        await safe_quit(driver=driver)

        return []
