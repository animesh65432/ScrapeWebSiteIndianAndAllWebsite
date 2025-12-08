from config.create_driver import create_driver
from config.safe_quit import safe_quit
from bs4 import BeautifulSoup
from .convert_to_markdown import convert_to_markdown
from utils.load_with_retry import load_with_retry
import asyncio

async def scrape_content(url):
    driver = None
    try:
        driver = await create_driver()

        if not await load_with_retry(driver, url,html_element="#row-content",part="north_India",retries=3, delay=3,isScraperAPIUsed=True):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            driver = None
            return None
        
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None

        soup = BeautifulSoup(html, 'html.parser')


        content_div = soup.find("div",{"id" :"row-content"})

        if not content_div:
            print("Content div not found")
            return None

        md_content = convert_to_markdown(content_div)
        
        return md_content

    except Exception as e:
        print("scrape_content error:", e)
        await safe_quit(driver=driver)
        driver = None
        return None