from config.create_driver import create_driver
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from utils.load_with_retry import load_with_retry
from datetime import datetime
from  config.safe_quit import safe_quit
import asyncio

async def scrape_website(url: str):
    driver = None

    try:
        driver = await create_driver(use_scraperapi=True)

        if not await load_with_retry(driver, url,html_element=".documents", part="northeast_india",retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            driver = None
            return []
        

        loop = asyncio.get_event_loop()

        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None

        soup = BeautifulSoup(html, "html.parser")

        announcements = []

        # Correct base URL
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        for doc in soup.select(".documents"):
            title_element = doc.select_one(".documents_title a")
            if not title_element:
                continue
            title = title_element.get_text(strip=True)
            pdf_link = title_element.get("href", "")

            time_element = doc.select_one(".documents_date time")
            date_str = time_element.get_text(strip=True) if time_element else ""
            date_obj = datetime.strptime(date_str, "%d-%b-%Y").date()
            today = datetime.today().date()
            if date_obj != today:
                continue

            
            if title and pdf_link:
                full_pdf_url = pdf_link if pdf_link.startswith("http") else urljoin(base_url, pdf_link)
                announcements.append({
                    "title": title,
                    "pdf_link": full_pdf_url,
                    "state" :"Assam"
                })

        return announcements

    except Exception as e:
        print("Scraping Error:", str(e))
        await safe_quit(driver=driver)
        return []
