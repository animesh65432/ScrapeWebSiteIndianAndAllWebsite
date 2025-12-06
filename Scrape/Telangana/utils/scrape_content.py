from bs4 import BeautifulSoup
from config.create_driver import create_driver
from  utils.load_with_retry import load_with_retry
from config.safe_quit import safe_quit

async def scrape_content(url):
    driver = None
    try:
        driver = await create_driver()

        if await load_with_retry(driver, url, html_element=".entry-content",retries=3, delay=3) is False:
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return ""

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract ONLY content
        content_div = soup.find("div", class_="entry-content")
        content = content_div.get_text("\n", strip=True) if content_div else ""


        return content

    except Exception as e:
        safe_quit(driver=driver)
        return f"scrape_telangana_content error occurred: {str(e)}"
