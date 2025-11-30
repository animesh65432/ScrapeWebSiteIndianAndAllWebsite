from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import re

def scrape_website(url):
    try :
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        driver.quit()

        annoucements_lists = soup.find("div", {"class" :"equal-height trasnitionAll"}).find_all("div",{"class" :"col-lg-3 col-md-3 col-sm-6 col-xs-12"})

        announcements = []

        for annoucement in annoucements_lists :
            title = annoucement.find("div",{"class" :"awardContent"}).find("h2").find("a").get_text(strip=True)
            link = annoucement.find("div",{"class" :"awardContent"}).find("h2").find("a")['href']
            match = re.search(r"\b\d{2}-\d{2}-\d{4}\b", title)

            if not match :
                continue

            date_str = match.group()

            parsed_date = datetime.strptime(date_str, "%d-%m-%Y").date()

            today = datetime.today().date()

            if parsed_date == today :
                announcements.append({
                    "title" : title,
                    "pdf_link"  : link,
                    "state" : "Uttarakhand"
                })


        return announcements
    except Exception as e:
        print("scrape_website error:", e)
        return None