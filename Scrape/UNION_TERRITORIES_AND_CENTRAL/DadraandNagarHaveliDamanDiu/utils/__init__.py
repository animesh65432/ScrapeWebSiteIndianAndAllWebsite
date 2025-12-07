from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime 
from config.create_driver import create_driver
from utils.load_with_retry import load_with_retry
from config.safe_quit import safe_quit
import asyncio

async def scrape_website(url: str):
    driver = None
    try:
        driver = await create_driver()

        if not await load_with_retry(driver, url, html_element=".data-table-1.doc-table.bt", retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            safe_quit(driver=driver)
            return []
        

        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None

        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find("table", {"class": "data-table-1 doc-table bt"})
        
        if not table:
            print("Table not found")
            return []
        
        annoucments_html_lists = table.find("tbody").find_all("tr")
        
       
        today = datetime.now().strftime("%d/%m/%Y")
        
        announcements = []
        
        for row in annoucments_html_lists:
            try:
                # Get all table data cells
                cells = row.find_all("td")
                
                if len(cells) >= 3:
                    # Extract title (first column)
                    title_cell = cells[0]
                    title_span = title_cell.find("span", class_="bt-content")
                    title = title_span.text.strip() if title_span else ""
                    
                    # Extract date (second column)
                    date_cell = cells[1]
                    date_span = date_cell.find("span", class_="bt-content")
                    announcement_date = date_span.text.strip() if date_span else ""
                    
                    if announcement_date == today:
                        # Extract PDF link (third column)
                        file_cell = cells[2]
                        pdf_link_tag = file_cell.find("a", href=True)
                        pdf_link = pdf_link_tag.get('href', '') if pdf_link_tag else ""
                        
                        announcement_data = {
                            'title': title,
                            'pdf_link': pdf_link,
                            'state' :"DadraandNagarHaveliDamanDiu"
                        }
                        
                        announcements.append(announcement_data)
                    
                        
            except Exception as row_error:
                print(f"Error parsing row: {row_error}\n")
                continue
        
        return announcements
        
    except Exception as e:
        print("scrape_website error:", e)
        await safe_quit(driver=driver)
        return []

