from bs4 import BeautifulSoup
from datetime import datetime
from config.create_driver import create_driver
from utils.load_with_retry import load_with_retry
from config.safe_quit import safe_quit
import asyncio

async def scrape_website(url):
    driver = None

    try:
        driver = await create_driver()
        
        if not await load_with_retry(driver, url, html_element=".news-item",retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []

        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)
        
        await safe_quit(driver=driver)
        driver = None

        soup = BeautifulSoup(html, 'html.parser')
        
        # Get yesterday's date in the format used on the website
        today = datetime.now().strftime("%B %d, %Y")
        
        notices = []
        news_items = soup.find_all('div', class_='news-item')

        
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
        
        
        if notices:
            return notices
        else:
            return []
            
    except Exception as e:
        print("scrape_website error:", e)
        await safe_quit(driver=driver)
        return []

