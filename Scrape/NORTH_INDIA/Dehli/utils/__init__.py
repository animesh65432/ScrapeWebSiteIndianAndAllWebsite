from config.create_driver import create_driver
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime 
import re
from utils.load_with_retry import load_with_retry
from config.safe_quit import safe_quit
import asyncio

async def scrape_website(url: str):
    driver = None
    try:
        driver = await create_driver()

        if not await load_with_retry(driver, url,html_element=".notification-view" ,retries=3, delay=3,isScraperAPIUsed=True):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []
    
        
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None
        
        soup = BeautifulSoup(html, "html.parser")

        
        results = []
        
        annpouncementshtmlLists = soup.find_all("div", {"class": "notification-view"})
        
        for li in annpouncementshtmlLists:
            title_el = li.select_one(".tab-title")
            date_el = li.select_one(".tab-date")
            
            if title_el:
                title_text = title_el.get_text(strip=True)
                title = re.sub(r'Date\s*:\s*\d{2}-\d{2}-\d{4}\s*\|\s*[\d.]+\s*(KB|MB|GB)', '', title_text).strip()
            else:
                title = None
            
            date = ""
            date_obj = None
            
            if date_el:
                date_text = date_el.get_text(strip=True)
                if "Date :" in date_text:
                    date = date_text.split(":")[1].split("|")[0].strip()
                    try:
                        date_obj = datetime.strptime(date, "%d-%m-%Y").date()
                    except ValueError:
                        date_obj = None
            
            
            link_el = soup.find("a",{"class":"tab-view"})
            
            link = urljoin(url, link_el.get("href")) if link_el and link_el.get("href") else ""
            
            if title and link and datetime.now().date() == date_obj :
                results.append({
                "title": title,
                "pdf_link": link,
                "state" :"Dehli"
                })
        
        return results
    except Exception as e:
        print("Scraping Error:", str(e))
        await safe_quit(driver=driver)
        return []