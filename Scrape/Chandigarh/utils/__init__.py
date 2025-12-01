from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse

def scrape_website(url: str):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        # Wait for content to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "views-row"))
        )
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        
        # Get today's date in the format DD-MM-YYYY
        today = datetime.now().strftime("%d-%m-%Y")
        
        view_content = soup.find("div", {"class": "view-content"})
        
        if not view_content:
            print("View content not found")
            return []
        
        annoucement_html_lists = view_content.find_all("div", {"class": "views-row"})
        
        announcements = []
        
        for row in annoucement_html_lists:
            try:
                # Extract date
                date_field = row.find("div", {"class": "views-field views-field-created"})
                date_span = date_field.find("span", {"class": "field-content"}) if date_field else None
                announcement_date = date_span.text.strip() if date_span else ""
                
                
                # Check if date matches today
                if announcement_date != today:
                    continue
                    # Extract title

                title_field = row.find("div", {"class": "views-field views-field-title"})
                title_link = title_field.find("a") if title_field else None
                title = title_link.text.strip() if title_link else ""
                    
                    # Extract PDF link from body field
                body_field = row.find("div", {"class": "views-field views-field-body"})
                pdf_link = ""
                    
                if body_field:
                    field_content = body_field.find("div", {"class": "field-content"})

                    if field_content:
                        
                        pdf_link_tag = field_content.find("a")
                        
                        if pdf_link_tag:
                            
                            pdf_link = pdf_link_tag.get('href', '')
                                
                            if pdf_link and not pdf_link.startswith('http'):
                                parsed_url = urlparse(url)
                                base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                                pdf_link = base_url + pdf_link
                    
                    
                    announcement_data = {
                        'title': title,
                        'pdf_link': pdf_link,
                        "state" :"Chandigarh"
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


