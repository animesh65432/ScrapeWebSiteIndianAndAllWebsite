from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime ,timedelta
from .scarpContent import scarpContent

def scrape_website(url: str):
    try:
        Chrome_Options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=Chrome_Options)
        driver.get(url)

        wait = WebDriverWait(driver, 30)

        # WAIT UNTIL loader disappears
        wait.until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "app-mini-loader .mini-loading"))
        )

        # Now page is fully loaded
        soup = BeautifulSoup(driver.page_source, "html.parser")

        driver.quit()

        table = soup.find("table", {"class": "table font-14 table-striped table_order_list table-custom table-custom"})

        announcements = []

        # Get current date components
        current_day = (datetime.now() - timedelta(days=1)).day
        
        # Month mapping from English to Hindi
        months_hindi = {
            1: "जनवरी", 2: "फरवरी", 3: "मार्च", 4: "अप्रैल",
            5: "मई", 6: "जून", 7: "जुलाई", 8: "अगस्त",
            9: "सितम्बर", 10: "अक्टूबर", 11: "नवम्बर", 12: "दिसम्बर"
        }
        
        current_month = months_hindi[datetime.now().month]
        current_year = datetime.now().year
        
        # Format: "28 नवम्बर 2025"
        today_date_str = f"{current_day} {current_month} {current_year}"

        announcements_lists = table.find("tbody").find_all("tr")

        for announcement in announcements_lists:
            tds = announcement.find_all("td")
            
            if len(tds) >= 4:
                date_time = tds[1].get_text(strip=True)
                title = tds[2].get_text(strip=True)
                detail_link = tds[3].find("a")
                
                # Extract just the date part (before comma)
                date_part = date_time.split(",")[0].strip()
                
                # Check if the date matches today's date
                if date_part == today_date_str and detail_link:
                    announcement_data = {
                        "title": title,
                        "detail_link": f"https://dipr.rajasthan.gov.in" + detail_link['href'] 
                    }
                    announcements.append(announcement_data)
        
        for annpouncement in announcements:
            content = scarpContent(annpouncement["detail_link"])
            annpouncement["content"] = content
      
    
        return announcements

    except Exception as e:
        print(f"Error in scrape_website: {e}")
        return None