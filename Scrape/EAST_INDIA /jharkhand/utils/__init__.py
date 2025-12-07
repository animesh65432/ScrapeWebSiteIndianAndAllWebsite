from config.create_driver import create_driver
from bs4 import BeautifulSoup
from datetime import datetime
from utils.load_with_retry import load_with_retry
from config.safe_quit import safe_quit
import asyncio

async def scrape_website(url: str) -> list:
    driver = None

    try:
        driver = await create_driver()

        if not await load_with_retry(driver, url, html_element="table.table-bordered.table-responsive",  retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []
        
        # Wait for table to load
        await asyncio.sleep(3)

        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None
        
        soup = BeautifulSoup(html, "html.parser")
        
        # Find the table with notices
        table = soup.find("table", {"class": "table table-bordered table-responsive"})
        
    
        if not table:
            print("Table not found!")
            return []
        
        notices = []
        rows = table.find("tbody").find_all("tr")
        
        # Calculate date range (yesterday to today)
        today = datetime.now().date()
        

        for row in rows:
            cells = row.find_all("td")
            
            if len(cells) >= 8:
                department = cells[1].get_text(strip=True)
                title = cells[2].get_text(strip=True)
                reference_date = cells[4].get_text(strip=True)
                
                # Extract view link
                view_link = cells[6].find("a")
                view_url = None
                if view_link:
                    href = view_link.get("href")
                    if href:
                        view_url = f"https://www.jharkhand.gov.in{href}" if href.startswith("/") else href
                
                # Date filtering
                try:
                    notice_date = datetime.strptime(reference_date, "%d/%m/%Y").date()
                    
                    # Skip if outside date range (yesterday to today)
                    if notice_date != today:
                        continue
                    
                    notice = {
                        "department": department,
                        "title": title,
                        "pdf_link": view_url,
                        "state": "Jharkhand"
                    }
                    
                    notices.append(notice)

                    
                except ValueError:
                    print(f"Invalid date format: {reference_date}")
                    continue
        
        return notices

    except Exception as e:
        print(f"Error: {e}")

        await safe_quit(driver=driver)

        return []

