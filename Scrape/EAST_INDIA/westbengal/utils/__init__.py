from config.create_driver import create_driver
from bs4 import BeautifulSoup
import re
from datetime import datetime
from utils.load_with_retry import load_with_retry
from config.safe_quit import safe_quit
import asyncio

async def scrape_website(url: str) -> dict:
    driver = None
    try:
        driver = await create_driver()
       
        html = driver.page_source


        if not await load_with_retry(driver, url,html_element="#ContentPlaceHolder1_grid_News" ,retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []
        
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None

        soup = BeautifulSoup(html, "html.parser")

        news_table = soup.find(id="ContentPlaceHolder1_grid_News")


        if not news_table:
            return []

        news_items = []
        tbody = news_table.find("tbody")
        rows = tbody.find_all("tr") if tbody else news_table.find_all("tr")
        
        today = datetime.now().date()

        for row in rows:
            if row.find("th"):
                continue

            date_tag = row.find("h5", class_="text-primary")
            content_tag = row.find("p", class_="text-muted")

            date_str = date_tag.get_text(strip=True) if date_tag else ""
            content = content_tag.get_text(strip=True) if content_tag else ""

            # Validate date string format
            if not re.match(r"^\d{2}-\d{2}-\d{4}$", date_str):
                continue

            news_date = datetime.strptime(date_str, "%d-%m-%Y").date()

            if news_date == today and content:
                news_items.append({
                    "content": content,
                    "state": "WestBengal",
                    "link": url,
                    "title" :content
                })

        return news_items

    except Exception as e:
        print(f"scrape_website error: {e}")
        await safe_quit(driver=driver)
        return []
