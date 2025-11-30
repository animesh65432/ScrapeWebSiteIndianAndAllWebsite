from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
from config.chromeOptions import Get_Chrome_Options


def scrape_Website(url: str):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        
        driver.get(url)
        html = driver.page_source
        driver.quit()
        
        soup = BeautifulSoup(html, "html.parser")
        
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
                
                
            
                if date_str == today:
                    today_news.append({
                        "title": title,
                        "link": link,
                        "state": "Maharashtra"
                    })
                    print(f"✓ Added: {title[:60]}...")
                    
            except Exception as e:
                print(f"Error parsing news card: {e}")
                continue
        
        print(f"\nTotal news items for today ({today}): {len(today_news)}")
        return today_news
        
    except Exception as e:
        print(f"Error in scrape_Website: {e}")
        return []

