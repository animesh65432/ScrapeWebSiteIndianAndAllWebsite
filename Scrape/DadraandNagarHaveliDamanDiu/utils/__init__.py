from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime 

def scrape_website(url: str):
    try:
        driver = webdriver.Chrome(options=Get_Chrome_Options())
        driver.get(url)
        
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "data-table-1"))
        )
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find("table", {"class": "data-table-1 doc-table bt"})
        
        if not table:
            print("Table not found")
            driver.quit()
            return []
        
        annoucments_html_lists = table.find("tbody").find_all("tr")
        driver.quit()
        
       
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
        if 'driver' in locals():
            driver.quit()
        return None

