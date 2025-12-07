from config.create_driver import create_driver
from bs4 import BeautifulSoup
from datetime import datetime
from utils.load_with_retry import load_with_retry
from config.safe_quit import safe_quit
import asyncio

async def scrape_website(url: str):
    driver = None
    try:
        driver = await create_driver()
        
        if not await load_with_retry(driver, url,html_element=".data-table-1" ,retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []
        
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)
        
        await safe_quit(driver=driver)
        driver = None

        soup = BeautifulSoup(html, 'html.parser')

        # Get current date in the format used by the website (DD/MM/YYYY)
        current_date = datetime.now().strftime("%d/%m/%Y")


        current_date_announcements = []
        table = soup.find('table', class_='data-table-1')
        
        if not table:
            print("No table found on the page")
            return []
        
        rows = table.find('tbody').find_all('tr')
        
        for row in rows:
            try:
                # Extract title
                title_cell = row.find('td', attrs={'data-th': 'Title '})
                title = title_cell.find('span', class_='bt-content').get_text(strip=True) if title_cell else None
                
                # Extract date
                date_cell = row.find('td', attrs={'data-th': 'Date '})
                date = date_cell.find('span', class_='bt-content').get_text(strip=True) if date_cell else None
                
                # Extract PDF link
                link_cell = row.find('td', attrs={'data-th': 'View / Download'})
                pdf_link = None
                if link_cell:
                    pdf_anchor = link_cell.find('a', attrs={'aria-label': lambda x: x and 'View' in x})
                    if pdf_anchor:
                        pdf_link = pdf_anchor.get('href')
                
                # Check if date is not current date

                if date and date == current_date:
                    announcement = {
                        'title': title,
                        'pdf_link': pdf_link,
                        "state" :"Bihar"
                    }
                    
                    
                    current_date_announcements.append(announcement)
                    
            except Exception as row_error:
                print(f"Error processing row: {row_error}")
                continue
        
        return current_date_announcements
        
    except Exception as e:
        await safe_quit(driver=driver)
        driver = None
        print(f"Bihar Utils scrape_website error: {e}")
        return []
