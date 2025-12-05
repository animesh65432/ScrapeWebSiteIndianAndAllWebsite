from bs4 import BeautifulSoup
from config.create_driver import create_driver
from utils.load_with_retry import load_with_retry
from urllib.parse import urljoin
from .scrape_content import scrape_content
from datetime import datetime
from  config.safe_quit import safe_quit
import asyncio

async def scrape_website(url):
    driver = None

    try:
       
        driver = await create_driver()
        

        if not await load_with_retry(driver, url, retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []
        

        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None

        soup = BeautifulSoup(html, "html.parser")

        announcements = []

        # Loop through each news item
        for li in soup.select("#lcp_instance_0 li"):
            a_tag = li.find("a")
            title = a_tag.get_text(strip=True) if a_tag else ""
            link = urljoin(url, a_tag['href']) if a_tag and a_tag.has_attr('href') else ""

            # Remove anchor text from li to get date text
            li_copy = BeautifulSoup(str(li), "html.parser")
            for a in li_copy.find_all("a"):
                a.extract()
            date_text = li_copy.get_text(strip=True)

            date_obj = datetime.strptime(date_text, "%B %d, %Y").date()
            
            today = datetime.today().date()

            if today == date_obj and  link and title:
                announcements.append({
                    "title": title,
                    "link": link,
                    "content": scrape_content(link),
                    "state" :"Goa"
                })

        return announcements

    except Exception as e:
        print(f"Scraping Error: {e}")

        await safe_quit(driver=driver)

        return None