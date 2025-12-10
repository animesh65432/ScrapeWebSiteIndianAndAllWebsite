from config.create_driver import create_driver
from bs4 import BeautifulSoup
from datetime import datetime
from .scrape_content import scrape_content
from utils.load_with_retry import load_with_retry
from config.safe_quit import safe_quit
import re
import asyncio

async def scrape_website(url:str):
    driver = None
    try:
        driver = await create_driver()

        if not await load_with_retry(driver, url,html_element="#page-content-block",part="northeast_india" ,retries=3, delay=3,):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            driver = None
            return []
        
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        soup = BeautifulSoup(html, 'html.parser')
        
        await safe_quit(driver=driver)
        driver = None

        annoucements_lists = soup.find("div",{"id":"page-content-block"}) \
                                 .find("ul",{"class":"archive"}) \
                                 .find_all("li")
        

        annoucements = []

        for annoucement in annoucements_lists:

            date_raw = annoucement.find("div", {"class": "list-item-category"}).get_text(strip=True)
            date_text = date_raw.split("Dated:")[1].strip()

           
            date_text = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_text)

          
            date_text = re.sub(r'(\d+)([A-Za-z]{3})', r'\1 \2', date_text)

         
            date_obj = datetime.strptime(date_text, "%d %b %y %I:%M %p")

            now = datetime.now()
            if date_obj.date() != now.date():
                continue

            title = annoucement.find("a").get_text(strip=True)
            link = "https://dipr.mizoram.gov.in/" + annoucement.find("a")["href"]

            if link :
                content =  await scrape_content(link)

            if content:
                annoucements.append({
                    "title": title,
                    "link": link,
                    "state": "Mizoram",
                    "content": content
                })
    

        return annoucements

    except Exception as e:
        await safe_quit(driver=driver)
        print(f"An error occurred: {str(e)}")
        return []
