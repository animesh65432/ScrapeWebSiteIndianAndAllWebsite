from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
from .scrape_content import scrape_content
import re

def scrape_website(url:str):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        annoucements_lists = soup.find("div",{"id":"page-content-block"}) \
                                 .find("ul",{"class":"archive"}) \
                                 .find_all("li")

        annoucements = []

        for annoucement in annoucements_lists:

            date_raw = annoucement.find("div", {"class": "list-item-category"}).get_text(strip=True)
            date_text = date_raw.split("Dated:")[1].strip()

           
            date_text = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_text)

          
            date_text = re.sub(r'(\d+)([A-Za-z]{3})', r'\1 \2', date_text)

         
            date_obj = datetime.strptime(date_text, "%d %b %y %I:%M %p")

            now = datetime.now()
            if date_obj.date() != now.date():
                continue

            title = annoucement.find("a").get_text()
            link = "https://dipr.mizoram.gov.in/" + annoucement.find("a")["href"]

            annoucements.append({
                "title": title,
                "link": link
            })
        
        for annoucement in annoucements:
            detailed_content = scrape_content(annoucement["link"])
            annoucement["content"] = detailed_content

        return annoucements

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
