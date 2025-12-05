from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_website(url):
    try:
        driver = webdriver.Chrome(options=Get_Chrome_Options())
        driver.set_page_load_timeout(120)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        
        Main = soup.find("main", {"id": "main"})
        Annoucementslists = Main.find("div", {"class": "listWrap"}).find_all("li")
        
        # Get current date in DD-MM-YYYY format
        current_date = datetime.now().strftime("%d-%m-%Y")
        
        # Array to store today's announcements
        announcements = []
        
        for announcement in Annoucementslists[1:]:
            title_tag = announcement.find("span", {"class": "tender-title"})
            department = announcement.find("span", {"class": "department"})
            
            # Get all spans with class "opening-date" - the last one is the publish date
            date_spans = announcement.find_all("span", {"class": "opening-date"})
            
            if title_tag and date_spans:
                # The last "opening-date" span contains the actual date
                date_text = date_spans[-1].get_text(strip=True)
                
                # Check if the announcement date matches current date
                if date_text == current_date:
                    title = title_tag.get_text(strip=True)
                    dept = department.get_text(strip=True) if department else "N/A"
                    
                    # Extract PDF link from the anchor tag
                    link_tag = title_tag.find("a")
                    pdf_link = link_tag.get("href") if link_tag else "N/A"

                    
                    announcement_data = {
                        "title": title,
                        "department": dept,
                        "pdf_link": pdf_link,
                        "state": "Punjab"
                    }
                    
                    announcements.append(announcement_data)
                
                   
        
        return announcements
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None