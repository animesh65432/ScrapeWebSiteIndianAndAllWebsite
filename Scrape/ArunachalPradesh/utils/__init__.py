from selenium import webdriver
from  config.chromeOptions import Get_Chrome_Options
from bs4 import BeautifulSoup
import time 
from datetime import datetime , timedelta

def scrape_website(url: str) -> list:
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        # Wait for content to load (adjust time if needed)
        time.sleep(3)
        
        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, "html.parser")
        
        # Find all table rows in tbody
        Annoucements = []
        table = soup.select_one(".table-container table tbody")
        
        if table:
            rows = table.find_all("tr")
            
            for row in rows:
                cols = row.find_all("td")
                
                if len(cols) >= 4:
                    title = cols[1].get_text(strip=True)
                    date_str = cols[2].get_text(strip=True)
                    
                    # Extract PDF link
                    link_tag = cols[3].find("a")
                    pdf_link = link_tag.get("href", "") if link_tag else ""

                    date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
                    
                    today = datetime.today().date()


                    if date_obj == today:
                        notice_data = {
                            "title": title,
                            "pdf_link":f"https://arunachalpradesh.gov.in/{pdf_link}",
                            "state" :"ArunachalPradesh"
                        }
                        Annoucements.append(notice_data)
        
        return Annoucements

    except Exception as e:
        print(f"Error: {e}")
        return None


















