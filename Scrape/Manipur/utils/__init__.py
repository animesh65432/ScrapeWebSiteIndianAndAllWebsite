from datetime import datetime
from utils.load_with_retry import load_with_retry
from bs4 import BeautifulSoup
from config.create_driver import create_driver
from config.safe_quit import safe_quit
import asyncio

async def scrape_website(url: str):
    driver = None
    try:
        driver = await create_driver()

        if not await load_with_retry(driver, url, retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            safe_quit(driver=driver)
            return None
        
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None
        
        soup = BeautifulSoup(html, "html.parser")
        
        # Get today's date in DD/MM/YYYY format (for Imphal West)
        today_slash = datetime.now().strftime("%d/%m/%Y")
        # Also get DD.MM.YYYY format (for Rajbhavan)
        today_dot = datetime.now().strftime("%d.%m.%Y")
        
        today_announcements = []
        
        # Try table-based layout first (Imphal West District)
        table = soup.find("table", class_="bt")
        if table:
            print("Found table layout")
            tbody = table.find("tbody")
            if tbody:
                rows = tbody.find_all("tr")
                print(f"Found {len(rows)} announcements")
                
                for row in rows:
                    try:
                        cells = row.find_all("td")
                        if len(cells) >= 3:
                            # Extract title
                            title_span = cells[0].find("span", class_="bt-content")
                            title = title_span.get_text(strip=True) if title_span else ""
                            
                            # Extract date
                            date_span = cells[1].find("span", class_="bt-content")
                            date_str = date_span.get_text(strip=True) if date_span else ""
                            
                            # Extract link
                            link_tag = cells[2].find("a")
                            link = link_tag.get("href", "") if link_tag else ""
                            
                            # Check if date matches today
                            if date_str == today_slash:
                                today_announcements.append({
                                    "title": title,
                                    "pdf_link": link,
                                    "state": "Manipur"
                                })
                                print(f"✓ Added: {title[:60]}...")
                                
                    except Exception as e:
                        print(f"Error parsing row: {e}")
                        continue
        
        # Try card-based layout (Rajbhavan)
        else:
            news_container = soup.find("div", class_="news-style-1 row news")
            if news_container:
                print("Found card layout")
                news_cards = news_container.find_all("div", class_="col-lg-3")
                print(f"Found {len(news_cards)} news items")
                
                for card in news_cards:
                    try:
                        # Extract title/link
                        title_tag = card.find("h2").find("a") if card.find("h2") else None
                        title = title_tag.get_text(strip=True) if title_tag else "No title"
                        link = title_tag.get("href", "") if title_tag else ""
                        
                        # Extract date from title (format: DD.MM.YYYY)
                        date_str = title.split(":")[0].strip() if ":" in title else ""

                        
                        # Check if date matches today
                        if date_str == today_dot:
                            today_announcements.append({
                                "title": title,
                                "pdf_link": link,
                                "state": "Manipur"
                            })
                           
                            
                    except Exception as e:
                        print(f"Error parsing card: {e}")
                        continue
        
        print(f"\nTotal announcements for today: {len(today_announcements)}")
        return today_announcements
        
    except Exception as e:
        print(f"Error in scrape_website: {e}")
        await safe_quit(driver=driver)
        return None