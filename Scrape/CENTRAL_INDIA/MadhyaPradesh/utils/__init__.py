from bs4 import BeautifulSoup
from datetime import datetime
from utils.hindi_months import hindi_months
from ..utils import scrape_content
from  config.create_driver import create_driver
from utils.load_with_retry import load_with_retry
from config.safe_quit import safe_quit
import asyncio

async def scrape_website(url: str):
    driver = None
    try:
        
        driver = await create_driver()

        if not await load_with_retry(driver, url,html_element="table", part="central_India",retries=3, delay=3,isdymainc=True):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []
        
        loop = asyncio.get_event_loop()


        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None       
        
        soup = BeautifulSoup(html, 'html.parser')


        table = soup.find('table', {"class" :"table table-striped table-bordered"})

        announcements_html_lists = table.find('tbody').find_all('tr')

        announcements = []

        for ann in announcements_html_lists:
            title = ann.find_all('td')[1].text.strip()
            date_str = ann.find_all('td')[2].text.strip()
            date_parts = date_str.replace(",", "").split()
            month = hindi_months[date_parts[1]]
            day = int(date_parts[2])
            year = int(date_parts[3])
            time_str = date_parts[4]
            dt = datetime.strptime(f"{day}-{month}-{year} {time_str}", "%d-%m-%Y %H:%M")
            today = datetime.now()
            link = ann.find_all('td')[1].find('a')['href'].strip()
            print(f"Found announcement: {title} dated {dt.date()} with link {link}")

            if today.date() == dt.date() and title and link:
                announcement = {
                    "title": title,
                    "link": link,
                    "state": "MadhyaPradesh",
                    "content": await scrape_content(link) 
                }

                announcements.append(announcement)
        
        return announcements
    except Exception as e:
        print(f"scrape_madhya_pradesh error: {e}")
        await safe_quit(driver=driver)
        driver = None
        return []

