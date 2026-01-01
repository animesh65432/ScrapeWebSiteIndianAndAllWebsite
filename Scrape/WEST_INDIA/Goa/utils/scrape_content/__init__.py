from bs4 import BeautifulSoup
import asyncio
from config.create_driver import create_driver
from config.safe_quit import safe_quit
from utils.load_with_retry import load_with_retry
from config.chromeOptions import Get_Chrome_Options
from .convert_to_markdown import convert_to_markdown


async def scrape_content(url):
    try:
        driver = await create_driver()

        if not await load_with_retry(driver, url, html_element=".cm-entry-title", retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return None
        
        loop = asyncio.get_event_loop()

        html = await loop.run_in_executor(None, lambda: driver.page_source)

        soup = BeautifulSoup(html, "html.parser")

        await safe_quit(driver=driver)


        # Extract title
        title = ""
        title_elem = soup.select_one(".cm-entry-title, h1.entry-title, .entry-title")
        if title_elem:
            title = title_elem.get_text(strip=True)

        # Extract date
        date = ""
        date_elem = soup.select_one("time.entry-date, .cm-post-date time")
        if date_elem:
            date = date_elem.get_text(strip=True)

        # Extract categories
        categories = []
        category_links = soup.select(".cm-post-categories a")
        categories = [cat.get_text(strip=True) for cat in category_links]

        # Get main content
        content_div = soup.select_one(".cm-entry-summary") or soup.select_one(".entry-content")
        
        if not content_div:
            print("Content div not found")
            return None

        # Convert to markdown
        markdown = convert_to_markdown(title, date, categories, content_div)
        
        return markdown

    except Exception as e:
        print(f"Error fetching content: {e}")
        
        await safe_quit(driver=driver)

        return None
