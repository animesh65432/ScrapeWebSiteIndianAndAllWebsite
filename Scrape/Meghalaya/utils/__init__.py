from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime,timedelta

def scapre_website(url:str):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(120)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        notification_div = soup.find("div", {"class": "notifications-view page-content-view border-content"})

        view_content = notification_div.find("div",{"class" : "view-content"})

        item_list = view_content.find("div" ,{"class" :"item-list"})
        
        annoucements_lists = item_list.find("ul").find_all("li")

        annoucements = []


        for annoucement in annoucements_lists :
            date_html = annoucement.find("span",{"class" :"views-field views-field-field-date1 field-color"}).find("small").get_text()
            date_str = date_html.split(":")[1].strip()
            date_obj = datetime.strptime(date_str, "%d %b %Y")

            today = datetime.today().date()
            date_only = date_obj.date()

            if today != date_only:
                continue

            title = annoucement.find("span",{"class" :"views-field views-field-title"}).find("span",{"class" : "field-content"}).find("a").get_text()
            pdf_link = annoucement.find("span" , {"class" : "field-content field-color"}).find("a")["href"]


            annoucements.append({
                "title" : title,
                "pdf_link" : pdf_link,
                "state" :"Meghalaya"
            })

        return annoucements
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
        return None