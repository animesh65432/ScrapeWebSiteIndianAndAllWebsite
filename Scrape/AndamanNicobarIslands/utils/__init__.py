from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

def scrape_website(url: str):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
      
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dataTables-example"))
        )
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find("table", {"class": "table table-striped table-bordered table-hover bt dataTable no-footer dtr-inline"})
        
        if not table:
            driver.quit()
            return []
        
        tbody = table.find("tbody")
        
        if not tbody:
            driver.quit()
            return []
        
        rows = tbody.find_all("tr")
        driver.quit()
        
        # Get today's date in DD-MM-YYYY format
        today = datetime.now().strftime("%d-%m-%Y")
        announcements = []
        
        for row in rows:
            try:
                # Get all table data cells
                cells = row.find_all("td")
                
                if len(cells) >= 4:
                    # Extract serial number (first column)
                    sl_no_cell = cells[0]
                    sl_no_span = sl_no_cell.find("span", class_="bt-content")
                    sl_no = sl_no_span.text.strip() if sl_no_span else ""
                    
                    # Extract subject/title (second column)
                    subject_cell = cells[1]
                    subject_span = subject_cell.find("span", class_="bt-content")
                    title = subject_span.text.strip() if subject_span else ""
                    
                    # Extract upload date (third column)
                    date_cell = cells[2]
                    date_span = date_cell.find("span", class_="bt-content")
                    upload_date = date_span.text.strip() if date_span else ""
                    
                    
                    # Check if date matches today
                    if upload_date == today:
                        # Extract PDF link (fourth column)
                        download_cell = cells[3]
                        download_span = download_cell.find("span", class_="bt-content")
                        
                        pdf_link = ""
                        if download_span:
                            pdf_link_tag = download_span.find("a", href=True)
                            if pdf_link_tag:
                                pdf_link = pdf_link_tag.get('href', '')
                                
                                # Make absolute URL if relative
                                if pdf_link and not pdf_link.startswith('http'):
                                    pdf_link = urljoin(url, pdf_link)
                        
                        announcement_data = {
                            'sl_no': sl_no,
                            'title': title,
                            'pdf_link': pdf_link,
                            'upload_date': upload_date
                        }
                        
                        announcements.append(announcement_data)
                        
            except :
                continue
    
        
        return announcements
        
    except Exception as e:
        if 'driver' in locals():
            driver.quit()
        return None
