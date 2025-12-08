from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config.create_driver import create_driver
from .scrape_content import scrape_content
from datetime import datetime
from utils.load_with_retry import load_with_retry
from  config.safe_quit import safe_quit
import asyncio

async def scraping_website(url):

    driver = None

    try:
        driver = await create_driver()

        if not await load_with_retry(driver, url,html_element=".modren" ,retries=3, delay=3,isScraperAPIUsed=True):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []
        
        loop = asyncio.get_event_loop()

        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None

        soup = BeautifulSoup(html, "html.parser")

        
        announcements = []

        for li in soup.select("li.modren"):
            a_tag = li.find("a")
            link = urljoin(url, a_tag['href']) if a_tag and a_tag.has_attr('href') else ""
            
            spans = li.find_all("span")
            title = spans[0].get_text(strip=True) if len(spans) > 0 else ""
            date_str = spans[-1].get_text(strip=True) if len(spans) > 1 else ""

            date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
            
            today = datetime.today().date()

            content = scrape_content(link)


            if today == date_obj and link and title and content:
                announcements.append({
                    "title": title,
                    "link": link,
                    "content": content ,
                    "state" :"HimachalPradesh"
                })


        return announcements

    except Exception as e:
        print(f"Scraping error: {e}")
        await safe_quit(driver=driver)
        return []
