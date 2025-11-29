from selenium import webdriver
from config.chromeOptions import Get_Chrome_Options
from bs4 import BeautifulSoup
import time
from datetime import datetime

def scrape_website(url: str) -> list:
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
                        "view_url": view_url,
                    }
                    
                    notices.append(notice)

                    
                except ValueError:
                    print(f"Invalid date format: {reference_date}")
                    continue
        
        return notices

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return []

