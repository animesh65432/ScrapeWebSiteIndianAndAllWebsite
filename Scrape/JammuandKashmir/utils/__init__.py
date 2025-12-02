from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
import requests
from typing import List, Dict
from datetime import datetime 

def scraping_website(url: str, base_url: str = None) -> List[Dict[str, str]]:
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
    
        html = driver.page_source

        soup = BeautifulSoup(html, "html.parser")

        driver.quit()
        
        # Find the table - it's inside section with id="tables"
        table_section = soup.find("section", id="tables")
        if not table_section:
            print("Table section not found")
            return []
        
        # Find the table within the section
        table = table_section.find("table")
        if not table:
            print("Table not found")
            return []
        
        notifications = []
        
        # Find all rows (skip header row)
        rows = table.find("tbody").find_all("tr")[1:]  # Skip first row (header)
        
        for row in rows:
            cols = row.find_all("td")
            
            if len(cols) >= 3:
                date_str = cols[0].get_text(strip=True)
                subject_cell = cols[2]
                link_tag = subject_cell.find("a")
                
                if link_tag:
                    subject = link_tag.get_text(strip=True)
                    pdf_link = link_tag.get("href", "")
                    
                    # Resolve relative URLs
                    if base_url and pdf_link:
                        pdf_link = urljoin(base_url, pdf_link)
                else:
                    subject = subject_cell.get_text(strip=True)
                    pdf_link = ""

                # Try both date formats (dots and slashes)
                try:
                    date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
                except ValueError:
                    try:
                        date_obj = datetime.strptime(date_str, "%d.%m.%Y").date()
                    except ValueError:
                        print(f"Could not parse date: {date_str}")
                        continue
                
                today = datetime.today().date()

                
                notification = {
                    "title": subject,
                    "pdf_link": pdf_link,
                    "state": "JammuandKashmir"
                }

                if date_obj == today:
                    notifications.append(notification)
        
        return notifications

    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None
    except Exception as e:
        print(f"Scraping error: {e}")
        return None
