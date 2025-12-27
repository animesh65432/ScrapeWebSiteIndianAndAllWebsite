from bs4 import BeautifulSoup
from config.create_driver import create_driver
from utils.load_with_retry import load_with_retry
from config.safe_quit import safe_quit
import asyncio

async def scrape_content(url):
    driver = None
    try:
        driver = await create_driver()
        
        if not await load_with_retry(driver, url, retries=3, delay=3,dont_use_proxy=True):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return None
        
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None

        # Use the fetched HTML, not driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        content_card = soup.find("div", class_="card-body")
        
        if content_card:
            content_div = content_card.find("div", style="text-align:justify")
            content_text = content_div.get_text(strip=True) if content_div else "No content found"
            return content_text.strip()
        else:
            return None
        
    except Exception as e:
        await safe_quit(driver=driver)
        print(f"Error during scraping: {str(e)}")
        return None
