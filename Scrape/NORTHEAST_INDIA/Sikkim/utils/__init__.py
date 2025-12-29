from bs4 import BeautifulSoup
from config.create_driver import create_driver
from urllib.parse import urljoin
from datetime import datetime
from .scrape_content import scrape_content
from utils.load_with_retry import load_with_retry
from  config.safe_quit import safe_quit
import asyncio

BASE_URL = "https://www.sikkim.gov.in"

async def scrape_website(url):
    driver = None
    try:
        driver = await create_driver()

        if not await load_with_retry(driver, url,html_element="table",part="northeast_india",retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []
        
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None
        
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", {"class": "table table-striped"})

        if not table:
            return []

        rows = table.find_all("tr")

        announcements = []

        # Format today date same as website ("26 Nov 2025")
        today = datetime.today().strftime("%d %b %Y")

        for row in rows:
            strong_tag = row.find("strong")
            if not strong_tag:
                continue  # skip empty rows

            # Extract title
            title = strong_tag.get_text(strip=True)

            # Extract date: example -> "-26 Nov 2025"
            date_items = row.find_all("li")
            if len(date_items) >= 2:
                raw_date = date_items[1].get_text(strip=True)
                clean_date = raw_date.replace("-", "").strip()  # "26 Nov 2025"
            else:
                clean_date = ""

            # Skip if date is empty or does NOT match today
            if clean_date != today:
                continue

            # Extract link
            link_tag = row.find("a", href=True)

            if link_tag:
                link = urljoin(BASE_URL, link_tag["href"])
            else:
                link = None
            
            if link:
                content = await scrape_content(link)

            if content:
                announcements.append({
                    "title": title,
                    "link": link,
                    "state": "Sikkim",
                    "content": content
                })

            
        return announcements

    except Exception as e:
        print(f"Error scraping Sikkim: {str(e)}")
        await safe_quit(driver=driver)
        return []
 
