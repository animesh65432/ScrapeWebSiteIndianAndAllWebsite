from config.create_driver import create_driver
from utils.load_with_retry import load_with_retry
from bs4 import BeautifulSoup
from datetime import datetime
from config.safe_quit import safe_quit
import asyncio

async def scrape_website(url: str):
    driver = None
    try:
        driver = await create_driver()

        if await load_with_retry(driver, url, retries=3, delay=3) is False:
            print("❌ Page failed to load after 3 retries")
            safe_quit(driver=driver)
            return None
        
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None
        
        soup = BeautifulSoup(html, 'html.parser')

        items_lists = soup.find("div", {"class": "view-content"}) \
                          .find("div", {"class": "item-list"}) \
                          .find_all("li")
        

        announcements = []

        today = datetime.today().date() 

        for item in items_lists:
            title = item.find("div", {"class": "views-field views-field-title"}) \
                        .find("span", {"class": "field-content"}) \
                        .get_text(strip=True)

            date_str = item.find("span", {"class": "date-display-single"}).get_text(strip=True)

            try:
                item_date = datetime.strptime(date_str, "%d/%m/%Y").date()
            except ValueError:
                print(f"Date parse error: {date_str}")
                continue

            pdf_div = item.find("div", {"class": "views-field views-field-field-upload-pdf"})
            pdf_link = pdf_div.find("a")['href'] if pdf_div and pdf_div.find("a") else None


            if item_date == today and pdf_link:
                announcements.append({
                    "title": title,
                    "pdf": pdf_link,
                    "state": "Puducherry"
                })

        return announcements

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        await safe_quit(driver=driver)
        return None
