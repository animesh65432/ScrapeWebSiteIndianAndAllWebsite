from config.create_driver import create_driver
from utils.load_with_retry import load_with_retry
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from .scrape_content import scrape_content
from config.safe_quit import safe_quit
import asyncio

async def scrape_website(url: str):
    driver = None
    try:
        driver = await create_driver()
        
        if await load_with_retry(driver, url, html_element=".elementor-post",part="south_india",retries=3, delay=3) is False:
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []
        
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        soup = BeautifulSoup(html, "html.parser")
        
        await safe_quit(driver=driver)
        driver = None

        # Best, reliable selector
        articleLists = soup.find_all("article", class_="elementor-post")

        announcements = []
        today = (datetime.today() - timedelta(days=2)).date()

        for article in articleLists:
            link = article.find("a")["href"]

            title = (
                article.find("h3", class_="elementor-post__title")
                .find("a")
                .get_text(strip=True)
            )

            date_str = article.find("span", class_="elementor-post-date").get_text(strip=True)

            # Convert to datetime
            try:
                parsed_date = datetime.strptime(date_str, "%B %d, %Y").date()
            except:
                continue

            # Check date match
            if parsed_date == today:
                announcements.append({
                    "title": title,
                    "link": link,
                    "state": "Telangana",
                    "content": await scrape_content(link)
                })

        # If no announcements for today
        if not announcements:
            return []

        return announcements

    except Exception as e:
        await safe_quit(driver=driver)
        print(f"scrape_website error occurred: {str(e)}")
        return []
