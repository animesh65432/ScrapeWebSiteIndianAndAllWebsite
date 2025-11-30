from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
from config.chromeOptions import Get_Chrome_Options

def scrape_website(url):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        # Wait for content to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "news-item"))
        )
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Get yesterday's date in the format used on the website
        today = datetime.now().strftime("%B %d, %Y")
        
        notices = []
        news_items = soup.find_all('div', class_='news-item')
        
        print(f"Found {len(news_items)} total news items")
        
        for item in news_items:
            try:
                # Find all paragraphs in the news item
                paragraphs = item.find_all('p')
                
                # The date is in the second paragraph, inside a span
                if len(paragraphs) >= 2:
                    date_paragraph = paragraphs[1]  # Second <p> tag contains the date
                    date_span = date_paragraph.find('span')
                    
                    if date_span:
                        notice_date = date_span.text.strip()
                        
                        # Check if date matches yesterday's date
                        if notice_date == today:
                            # Extract title and PDF link from first paragraph
                            first_paragraph = paragraphs[0]
                            link_tag = first_paragraph.find('a')
                            
                            if link_tag:
                                title = link_tag.text.strip()
                                pdf_link = link_tag.get('href', '')
                                
                                # Make absolute URL if relative
                                if pdf_link and not pdf_link.startswith('http'):
                                    base_url = 'http://csharyana.gov.in'
                                    pdf_link = base_url + pdf_link
                                
                                notice_data = {
                                    'title': title,
                                    'pdf_link': pdf_link,
                                    'state': "Haryana"
                                }
                                notices.append(notice_data)
                                print(f"✓ Added: {title[:50]}...")
            
            except Exception as e:
                print(f"Error parsing news item: {e}")
                continue
        
        driver.quit()
        
        if notices:
            return notices
        else:
            return []
            
    except Exception as e:
        print("scrape_website error:", e)
        if 'driver' in locals():
            driver.quit()
        return None

