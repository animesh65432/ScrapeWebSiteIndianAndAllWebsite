from bs4 import BeautifulSoup
from datetime import datetime
from config.create_driver import create_driver
from utils.load_with_retry import load_with_retry
import re
from config.safe_quit import safe_quit
import asyncio

async def scrape_website(url: str):
    driver = None
    try:
        driver = await create_driver()
        
        if not await load_with_retry(driver, url,html_element="table",retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []
        
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        soup = BeautifulSoup(html, "html.parser")

        await safe_quit(driver=driver)

        driver = None

        announcements = []

        table = soup.find("table", class_="table table-bordered table-hover cols-3")
        if not table:
            return []

        rows = table.find("tbody").find_all("tr")


        today = datetime.today().date()

        for row in rows:
           
            title_cell = row.find("td", class_="views-field-title")
            if not title_cell:
                continue

            title = title_cell.get_text(strip=True)



            # Extract "Dated 15th November, 2025"
            match = re.search(r"Dated\s+(\d{1,2}(st|nd|rd|th)?\s+\w+,\s+\d{4})", title)
            if not match:
                continue

            date_str = match.group(1)

            # Remove st/nd/rd/th
            cleaned = re.sub(r"(st|nd|rd|th)", "", date_str)

           
            parsed_date = datetime.strptime(cleaned.strip(), "%d %B, %Y").date()

            link_cell = row.find("td", class_="views-field-field-upload-pdf")
            if not link_cell:
                continue

            link = link_cell.find("a")["href"]
            if link.startswith("/"):
                link = "https://tripura.gov.in" + link

            if parsed_date == today:
                announcements.append({
                    "title": title,
                    "pdf_link": link,
                    "state": "Tripura"
                })

        return announcements

    except Exception as e:
        print(f"scrape_website error occurred: {str(e)}")
        await safe_quit(driver=driver)
        return []
