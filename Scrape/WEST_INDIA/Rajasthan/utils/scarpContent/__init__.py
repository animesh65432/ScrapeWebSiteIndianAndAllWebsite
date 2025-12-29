from bs4 import BeautifulSoup
from config.safe_quit import safe_quit
from config.create_driver import create_driver
from utils.load_with_retry import load_with_retry
import asyncio

async def scarpContent(url: str):
    driver = None
    try:
        driver = await create_driver()

        # Wait for main content to appear
        if not await load_with_retry(
            driver, 
            url,
            html_element="div",  # corrected
            retries=3, 
            delay=3,
        ):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return None


        loop = asyncio.get_event_loop()

        # Get final HTML
        html = await loop.run_in_executor(None, lambda: driver.page_source)
        soup = BeautifulSoup(html, "html.parser")

        await safe_quit(driver=driver)
        driver = None

        # Extract clean content
        content_divs = soup.select("div.press-release-details-left div")

        content = "\n".join(
            d.get_text(" ", strip=True)
            for d in content_divs
            if d.get_text(strip=True)
        )

        return content

    except Exception as e:
        await safe_quit(driver=driver)
        print(f"Error: {e}")
        return None
