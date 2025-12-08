from config.create_driver import create_driver
from utils.load_with_retry import load_with_retry
from bs4 import BeautifulSoup
from datetime import datetime
from .scrape_content import scrape_content
from config.safe_quit import safe_quit
import re
import asyncio

async def scrape_website(url):
    driver = None
    try :
        driver = await create_driver()

        if not await load_with_retry(driver, url,html_element="div.equal-height" ,retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []
        
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)
        
        soup = BeautifulSoup(html, 'html.parser')

        await safe_quit(driver=driver)
        driver = None

        annoucements_lists = soup.find("div", {"class" :"equal-height trasnitionAll"}).find_all("div",{"class" :"col-lg-3 col-md-3 col-sm-6 col-xs-12"})

        announcements = []

        for annoucement in annoucements_lists :
            title = annoucement.find("div",{"class" :"awardContent"}).find("h2").find("a").get_text(strip=True)
            link = annoucement.find("div",{"class" :"awardContent"}).find("h2").find("a")['href']
            match = re.search(r"\b\d{2}-\d{2}-\d{4}\b", title)

            if not match :
                continue

            date_str = match.group()

            parsed_date = datetime.strptime(date_str, "%d-%m-%Y").date()

            today = datetime.today().date()

            if parsed_date == today  and link:
                announcements.append({
                    "title" : title,
                    "link"  : link,
                    "state" : "Uttarakhand",
                    "content" : await scrape_content(link)
                })
    
        return announcements
    except Exception as e:
        print("scrape_website error:", e)
        await safe_quit(driver=driver)
        return []