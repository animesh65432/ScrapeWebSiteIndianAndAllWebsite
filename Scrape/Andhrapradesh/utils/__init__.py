from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time

def scrape_website(url: str, days_back: int = 0):
   
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        # Wait for page to load
        wait = WebDriverWait(driver, 10)
        
        # Calculate date range (excluding today)
        current_date = datetime.now()
        to_date_obj = current_date - timedelta(days=1)  # Yesterday
        from_date_obj = current_date - timedelta(days=days_back)  # X days back
        
        # Format dates as DD-MM-YYYY (format used by the site)
        from_date = from_date_obj.strftime("%d-%m-%Y")
        to_date = to_date_obj.strftime("%d-%m-%Y")
        
        
        try:
            # Fill in the date fields
            from_date_input = wait.until(
                EC.presence_of_element_located((By.ID, "txtfrmdate"))
            )
            to_date_input = driver.find_element(By.ID, "txttodate")
            
            # Clear existing values and enter new dates
            from_date_input.clear()
            from_date_input.send_keys(from_date)
            
            to_date_input.clear()
            to_date_input.send_keys(to_date)
            
           
            
            # Click the Search button
            search_button = driver.find_element(By.ID, "BtnSearch")
            search_button.click()
            
            
            
            # Wait for results to load (wait for table or any result element)
            time.sleep(3)  # Give time for results to load
            
            # Get the page source after search
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Extract announcements (no date filtering needed)
            announcements = extract_announcements(soup)
            
            driver.quit()
            return announcements if announcements else []
            
        except Exception as e:
            print(f"Error during form interaction: {e}")
            driver.quit()
            return []
        
    except Exception as e:
        print(f"Andhra Pradesh Utils scrape_website error: {e}")
        return []


def extract_announcements(soup):
 
    announcements = []
    
    try:
        # Look for the results table
        tables = soup.find_all('table', class_='Grid')
        
        if not tables:
            tables = soup.find_all('table')
           
        
        for table in tables:
            rows = table.find_all('tr')
           
            
            for row in rows:
                try:
                    cells = row.find_all('td')
                    
                    # Skip header rows
                    if not cells or len(cells) < 3:
                        continue
                    
                    # Extract data from cells
                    go_number = cells[1].get_text(strip=True) if len(cells) > 1 else ""
                    go_date = cells[2].get_text(strip=True) if len(cells) > 2 else ""
                    title = cells[4].get_text(strip=True) if len(cells) > 4 else ""
                    
                    # Look for PDF link in multiple ways
                    pdf_link = None
                    links = row.find_all('a')
                    
                    # Debug: Print first link details for first few rows
                    if len(announcements) < 3 and links:
                        print(f"  DEBUG - Link found: onclick={links[0].get('onclick', 'N/A')[:50]}, href={links[0].get('href', 'N/A')[:50]}")
                    
                    for link in links:
                        # Method 1: Check onclick attribute
                        onclick = link.get('onclick', '')
                        if 'downloadFile' in onclick:
                            import re
                            match = re.search(r'downloadFile\(["\'](\d+)["\']', onclick)
                            if match:
                                file_id = match.group(1)
                                pdf_link = f"https://goir.ap.gov.in/dgo.ashx?gid={file_id}&fileType=E"
                                break
                        
                        # Method 2: Check href attribute
                        href = link.get('href', '')
                        if 'downloadFile' in href:
                            import re
                            match = re.search(r'downloadFile\(["\'](\d+)["\']', href)
                            if match:
                                file_id = match.group(1)
                                pdf_link = f"https://goir.ap.gov.in/dgo.ashx?gid={file_id}&fileType=E"
                                break
                        
                        # Method 3: Check for direct download links
                        if 'dgo.ashx' in href or '.pdf' in href.lower():
                            if href.startswith('http'):
                                pdf_link = href
                            else:
                                pdf_link = f"https://goir.ap.gov.in{href}"
                            break
                    
                    # Add all announcements
                    
                    if title and go_date:
                        announcement = {
                            'title': title,
                            'pdf_link': pdf_link,
                            'state' :"Andhrapradesh"
                        }
                        announcements.append(announcement)
                        
                        # Show status
                        link_status = "✓ [PDF]" if pdf_link else "⚠ [No PDF]"
                        print(f"{link_status} {go_number} | {go_date} | {title[:60]}...")
                        
                except Exception as row_error:
                    print(f"Error processing row: {row_error}")
                    continue
        
        
    except Exception as e:
        print(f"Error extracting announcements: {e}")
    
    return announcements
