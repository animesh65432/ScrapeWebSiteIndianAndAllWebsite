from selenium import webdriver
from config.chromeOptions import Get_Chrome_Options
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta

def scrape_website(url: str) -> list:
    """
    Scrape notices from Jharkhand government portal
    
    Args:
        url: The URL to scrape (e.g., "https://www.jharkhand.gov.in/Home/DocumentList")
    
    Returns:
        List of dictionaries containing notice information from yesterday and today
    """
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        # Wait for table to load
        time.sleep(3)
        
        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, "html.parser")
        
        # Find the table with notices
        table = soup.find("table", {"class": "table table-bordered table-responsive"})
        
        if not table:
            print("Table not found!")
            return []
        
        notices = []
        rows = table.find("tbody").find_all("tr")
        
        # Calculate date range (yesterday to today)
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        # Set time to start and end of day for proper comparison
        start_dt = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        end_dt = today.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        print(f"Filtering notices from {start_dt.strftime('%d/%m/%Y')} to {end_dt.strftime('%d/%m/%Y')}")
        
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
                    notice_date = datetime.strptime(reference_date, "%d/%m/%Y")
                    
                    # Skip if outside date range (yesterday to today)
                    if notice_date < start_dt or notice_date > end_dt:
                        continue
                    
                    notice = {
                        "department": department,
                        "title": title,
                        "reference_date": reference_date,
                        "view_url": view_url,
                    }
                    
                    notices.append(notice)

                    
                except ValueError:
                    # Skip if date parsing fails
                    print(f"Could not parse date: {reference_date}")
                    continue
        
        return notices

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return []

