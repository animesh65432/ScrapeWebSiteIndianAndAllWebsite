from selenium import webdriver
from config.chromeOptions import Get_Chrome_Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime 
import re

def scrape_website(url: str):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".tab-date"))
        )
        
        html = driver.page_source
        
        driver.quit()
        
        soup = BeautifulSoup(html, "html.parser")
        
        results = []
        
        annpouncementshtmlLists = soup.find_all("div", {"class": "notification-view"})
        
        for li in annpouncementshtmlLists:
            title_el = li.select_one(".tab-title")
            date_el = li.select_one(".tab-date")
            
            if title_el:
                title_text = title_el.get_text(strip=True)
                title = re.sub(r'Date\s*:\s*\d{2}-\d{2}-\d{4}\s*\|\s*[\d.]+\s*(KB|MB|GB)', '', title_text).strip()
            else:
                title = None
            
            date = ""
            date_obj = None
            
            if date_el:
                date_text = date_el.get_text(strip=True)
                if "Date :" in date_text:
                    date = date_text.split(":")[1].split("|")[0].strip()
                    try:
                        date_obj = datetime.strptime(date, "%d-%m-%Y").date()
                    except ValueError:
                        date_obj = None
            
            
            link_el = soup.find("a",{"class":"tab-view"})
            
            link = urljoin(url, link_el.get("href")) if link_el and link_el.get("href") else ""
            
            if title and link and datetime.now().date() == date_obj :
                results.append({
                "title": title,
                "link": link
                })
        
        return results
    except Exception as e:
        print("Scraping Error:", str(e))
        return None