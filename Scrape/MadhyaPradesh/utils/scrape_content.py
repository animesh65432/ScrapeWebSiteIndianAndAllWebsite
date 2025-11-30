from selenium import webdriver
from config.chromeOptions import Get_Chrome_Options
from bs4 import BeautifulSoup
import time

def scrape_content(url:str):
    driver = None
    print(f"Scraping content from: {url}")
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        
        time.sleep(3)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        driver.quit()
        
        
        news_details = soup.find("p", {"id": "newsdetails"})
        
        if not news_details:
            print("Content not found")
            return None
        
       
        content_paragraphs = news_details.find_all("p", class_="MsoNormal")
        
        if content_paragraphs:
            content = "\n\n".join([p.get_text(strip=True) for p in content_paragraphs])
        else:
            content = news_details.get_text(separator="\n", strip=True)
        
       
        content = "\n".join([line.strip() for line in content.split("\n") if line.strip()])
        
        return content
        
    except Exception as e:
        print("Error in scrape_content:", e)
        return None
   