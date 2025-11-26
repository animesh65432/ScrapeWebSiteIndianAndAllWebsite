from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
from config.chromeOptions import Get_Chrome_Options

def scrape_website(url: str):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        
        driver.get(url)
        html = driver.page_source
        driver.quit()
        
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
                                    "date": date_str,
                                    "title": title,
                                    "link": link,
                                    "type": "table"
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
                        
                        # Extract image
                        img_tag = card.find("img")
                        image_url = img_tag.get("src", "") if img_tag else ""
                        
                        # Extract description
                        desc_tag = card.find("p")
                        description = desc_tag.get_text(strip=True) if desc_tag else ""
                        
                        # Check if date matches today
                        if date_str == today_dot:
                            today_announcements.append({
                                "date": date_str,
                                "title": title,
                                "link": link,
                                "image": image_url,
                                "description": description,
                                "type": "card"
                            })
                            print(f"✓ Added: {title[:60]}...")
                            
                    except Exception as e:
                        print(f"Error parsing card: {e}")
                        continue
        
        print(f"\nTotal announcements for today: {len(today_announcements)}")
        return today_announcements
        
    except Exception as e:
        print(f"Error in scrape_website: {e}")
        return []