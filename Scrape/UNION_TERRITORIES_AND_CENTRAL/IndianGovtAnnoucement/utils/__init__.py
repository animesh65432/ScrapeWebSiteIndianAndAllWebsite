from urllib.parse import urljoin
from config.create_driver import create_driver
from utils.load_with_retry import load_with_retry
from bs4 import BeautifulSoup
from .scrape_content import scrape_content
from config.safe_quit import safe_quit
import asyncio

async def scrape_website(url:str,base_url:str="https://www.pib.gov.in/Allrel.aspx"):
    driver = None
    try:
        driver = await create_driver()
        
        if not await load_with_retry(driver, url,html_element="li", retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []
        
        
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None

        soup = BeautifulSoup(html, 'html.parser')


        announcements = []
        
        office_sections = soup.find_all("li")


        for section in office_sections:
            office_name_tag = section.find("h3", class_="font104")
            release_list = section.find("ul", class_="num")
            
            if not office_name_tag or not release_list:
                continue
            
            announcement_type = office_name_tag.get_text(strip=True)
            
            for li in release_list.find_all("li"):
                link_elem = li.find("a")
                
                if not link_elem:
                    continue
                
                title = link_elem.get("title") or link_elem.get_text(strip=True)
                
                href = link_elem.get("href")
                
                if href:
                    href = urljoin(base_url, href)
                
                content = None
                
                if not href:
                    continue
                else :
                    content = await scrape_content(href)
                    
                announcements.append({
                    "department": announcement_type,
                    "title": title.strip(),
                    "link": href,
                    "content": content,
                    "state": "IndianGovt"
                })
        
        return announcements
    
    except Exception as e:

        print("scrape_website", e)

        await safe_quit(driver=driver)

        return []