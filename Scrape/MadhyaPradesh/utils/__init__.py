from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
from utils.hindi_months import hindi_months
from Scrape.MadhyaPradesh.utils.scrape_content import scrape_content
import time

def scrape_website(url: str):
    driver = None
    try:
        print(f"Loading Madhya Pradesh page: {url}")
        driver = webdriver.Chrome(options=Get_Chrome_Options())
        driver.get(url)
        
        # Wait for the AJAX content to load
        print("Waiting for AJAX content to load...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "ajaxdata"))
        )
        
        # Give it extra time for the AJAX call to complete
        time.sleep(3)
        
        # Wait for actual content inside ajaxdata div
        WebDriverWait(driver, 10).until(
            lambda d: len(d.find_element(By.ID, "ajaxdata").text.strip()) > 0
        )
        
        print("AJAX content loaded, parsing...")
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        driver.quit()


        table = soup.find('table', {"class" :"table table-striped table-bordered"})

        announcements_html_lists = table.find('tbody').find_all('tr')

        announcements = []

        for ann in announcements_html_lists:
            title = ann.find_all('td')[1].text.strip()
            date_str = ann.find_all('td')[2].text.strip()
            date_parts = date_str.replace(",", "").split()
            month = hindi_months[date_parts[1]]
            day = int(date_parts[2])
            year = int(date_parts[3])
            time_str = date_parts[4]
            dt = datetime.strptime(f"{day}-{month}-{year} {time_str}", "%d-%m-%Y %H:%M")
            today = datetime.now()
            link = ann.find_all('td')[1].find('a')['href'].strip()

            if today.date() == dt.date() and title and link:
                announcement = {
                    "title": title,
                    "link": link,
                    "state": "MadhyaPradesh"
                }

                announcements.append(announcement)
    

        for ann in announcements:
            ann["content"] = scrape_content(ann["link"])

        
        return announcements
        
    except Exception as e:
        print(f"scrape_madhya_pradesh error: {e}")
        return None

