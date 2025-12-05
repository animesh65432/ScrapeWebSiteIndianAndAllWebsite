from datetime import datetime
from config.create_driver import create_driver
from bs4 import BeautifulSoup
from urllib.parse import quote
from utils.load_with_retry import load_with_retry
from config.safe_quit import safe_quit
import asyncio

async def scarp_website(url: str):
    driver = None
    try:
        driver = await create_driver()
        
        if not await load_with_retry(driver, url, retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []

        # Parse HTML
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None

        soup = BeautifulSoup(html, 'html.parser')

        # Find table rows
        table_body = soup.find("table",{"id" :"my-table"}).find("tbody")

        

        announcement_rows = table_body.find_all("tr")

    
        # Today's date in the format used in the table
        today_str = datetime.today().strftime("%d-%m-%Y")


        today_announcements = []

        for row in announcement_rows:
            cols = row.find_all("td")
            if len(cols) < 4:
                continue

            serial = cols[0].text.strip()
            title_tag = cols[1].find("a")
            title = title_tag.text.strip() if title_tag else cols[1].text.strip()
            category = cols[2].text.strip()
            date = cols[3].text.strip()
            link_tag = cols[4].find("a")
            link = link_tag['href'] if link_tag else (f"{url}{title_tag['href']}" if title_tag else "")
            if link.startswith("/"):
                link = f"https://nagaland.gov.in{link}"
            
            safe_url = quote(link, safe=":/")

            if date == today_str and title and link:
                today_announcements.append({
                    "title": title,
                    "department": category,
                    "pdf_link": safe_url,
                    "state": "Nagaland",
                })

        return today_announcements

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        await safe_quit(driver=driver)
        return None
    