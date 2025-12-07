from config.create_driver import create_driver
from utils.load_with_retry import load_with_retry
from bs4 import BeautifulSoup
from datetime import datetime
from config.safe_quit import safe_quit
import asyncio

async def scrape_website(url):
    driver = None
    try:
        driver = await create_driver()
    
        if not await load_with_retry(driver, url,html_element=".tableData", retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []
        
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None

        soup = BeautifulSoup(html, 'html.parser')

        
        table = soup.find("table", {"class": "tableData DocumentTable"})

        if not table:
            print("Table not found")
            return []

        rows = table.find("tbody").find_all("tr")
        announcements = []
        today = datetime.today().date()

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 6:
                continue

            title = cols[4].get_text(strip=True)
            date_str = cols[2].get_text(strip=True)  # E.g., 03/03/2025

            # Skip blank dates
            if not date_str or date_str == "-":
                continue

            try:
                date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()

                if date_obj == today:
                    pdf_link = None
                    link_tag = cols[5].find("a")
                    if link_tag:
                        pdf_link = link_tag.get("href")

                    announcements.append({
                        'title': title,
                        'pdf_link':f"https://gad.gujarat.gov.in/personnel/{pdf_link}",
                        'state': "Gujarat"
                    })

            except Exception as e:
                print(f"Invalid date format: {date_str} - {e}")
                continue

        print(f"\nTotal announcements matching today's date: {len(announcements)}")
        return announcements

    except Exception as e:
        print("scrape_website", e)
        await safe_quit(driver=driver)
        return []
