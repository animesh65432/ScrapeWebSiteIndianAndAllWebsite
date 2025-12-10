from datetime import datetime
from utils.load_with_retry import load_with_retry
from bs4 import BeautifulSoup
from config.create_driver import create_driver
from .scrape_content import scrape_content
from config.safe_quit import safe_quit
import asyncio

async def scrape_Website(url: str):
    driver = None
    try:
        driver = await create_driver()

        if not await load_with_retry(driver, url,html_element=".news-style-1" ,retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            driver = None
            return []
        
        loop = asyncio.get_event_loop()
        
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        soup = BeautifulSoup(html, "html.parser")

        await safe_quit(driver=driver)

        driver = None
        
        
        # Find the parent container that holds all news items
        news_container = soup.find("div", class_="news-style-1 row news")
        
        if not news_container:
            print("No news container found")
            return []
        
        # Find all individual news cards
        news_cards = news_container.find_all("div", class_="col-lg-3 col-md-3 col-sm-6 col-xs-12")
    

        print(f"Found: {len(news_cards)} news items")
        
        today = datetime.now().strftime("%d.%m.%Y")
        today_news = []
        
        for card in news_cards:
            try:
                # Extract the title/link
                title_tag = card.find("h2").find("a")
                title = title_tag.get_text(strip=True) if title_tag else "No title"
                link = title_tag.get("href", "") if title_tag else ""
                
                # Extract date from title (format: DD.MM.YYYY)
                date_str = title.split(":")[0].strip() if ":" in title else ""

                
                if date_str == today and link:
                    today_news.append({
                        "title": title,
                        "link": link,
                        "state": "Maharashtra",
                        "content":  await scrape_content(link)
                    })
                    
            except Exception as e:
                print(f"Error parsing news card: {e}")
                continue
        
        
        return today_news
        
    except Exception as e:
        print(f"Error in scrape_Website: {e}")
        await safe_quit(driver=driver)
        driver = None
        return []

