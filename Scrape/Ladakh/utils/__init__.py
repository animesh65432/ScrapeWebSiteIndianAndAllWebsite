from datetime import datetime
from utils.load_with_retry import load_with_retry
from bs4 import BeautifulSoup
from config.create_driver import create_driver
from config.safe_quit import safe_quit
import asyncio

async def scrape_website(url: str):
    driver = None
    try:
        driver = await create_driver()

        if not await load_with_retry(driver, url, retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []
        
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)

        driver = None

        soup = BeautifulSoup(html, "html.parser")


        table = soup.find("table")


        if not table:
            print("No table found")
            return []

        rows = table.find("tbody").find_all("tr")

        today = datetime.today().date()  # today

        announcements = []

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 3:
                continue

            title = cols[0].get_text(strip=True)

            date_text = cols[1].get_text(strip=True) 

            if not date_text:
                print("Skipping row: empty date",date_text)
                continue

            parsed_date = datetime.strptime(date_text, "%d/%m/%Y").date()

            # Skip if not today

            if parsed_date != today:
                continue

            # Get PDF link
            link_tag = cols[2].find("a", href=True)
            link = link_tag["href"] if link_tag else None


            announcements.append({
                "title": title,
                "pdf_link": link,
                "state": "Ladakh"
            })

        return announcements

    except Exception as e:
        print(f"Error: {e}")
        await safe_quit(driver=driver)
        return None
