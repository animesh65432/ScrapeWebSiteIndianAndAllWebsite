from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from config.create_driver import create_driver
from datetime import datetime
from utils.load_with_retry import load_with_retry
from config.safe_quit import safe_quit
import asyncio

async def scrape_website(url):
    driver = None
    try:
        driver = await create_driver()

        if not await load_with_retry(driver, url,html_element = "table.bt tbody tr", retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []
    

        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None

        soup = BeautifulSoup(html, 'html.parser')

        # Get current date
        current_date = datetime.now()
        print(f"Current Date: {current_date.strftime('%d/%m/%Y')}\n")

        table = soup.find("table", {"class": "bt"})
        
        if not table:
            print("Table not found")
            return []

        annoucement_html_lists = table.find("tbody").find_all("tr")
        print(f"Found {len(annoucement_html_lists)} rows in table\n")

        announcements = []

        for row in annoucement_html_lists:
            try:
                # Get all table data cells
                cells = row.find_all("td")
                
                if len(cells) >= 5:
                    # Extract title
                    title_cell = cells[0]
                    title_span = title_cell.find("span", class_="bt-content")
                    title = title_span.text.strip() if title_span else ""
                    
                    
                    # Extract start date
                    start_date_cell = cells[2]
                    start_date_span = start_date_cell.find("span", class_="bt-content")
                    start_date_str = start_date_span.text.strip() if start_date_span else ""
                    
                    # Extract end date
                    end_date_cell = cells[3]
                    end_date_span = end_date_cell.find("span", class_="bt-content")
                    end_date_str = end_date_span.text.strip() if end_date_span else ""
                    
                    # Extract PDF link
                    file_cell = cells[4]
                    pdf_link_tag = file_cell.find("a", class_="pdf-download-link")
                    pdf_link = pdf_link_tag.get('href', '') if pdf_link_tag else ""
                    
                    # Parse dates (format: DD/MM/YYYY)
                    try:
                        start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
                        end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
                        # Check if current date is within the valid range
                        if start_date <= current_date <= end_date:
                            announcement_data = {
                                'title': title,
                                'pdf_link': pdf_link,
                                'state' :'Lakshadweep'
                            }
                            announcements.append(announcement_data)
                            
                    except ValueError as date_error:
                        print(f"Date parsing error: {date_error} - {start_date_str} to {end_date_str}")
                        continue
                        
            except Exception as row_error:
                print(f"Error parsing row: {row_error}")
                continue
            
        return announcements
        
    except Exception as e:
        print("scrape_website", e)
        await safe_quit(driver=driver)
        return None

