from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime

def scapre_website(url:str):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        annoucements_lists = soup.find("table",{"class":"views-table sortable views-view-table cols-5"}).find("tbody").find_all("tr")

        annocuements = []

        for annoucement in annoucements_lists:
            title = annoucement.find("td",{"class" :"views-field views-field-title"}).get_text(strip=True)
            date_str = annoucement.find("td",{"class" :"views-field views-field-field-date"}).get_text(strip=True)
            pdf_link = annoucement.find("td",{"class" :"views-field views-field-nothing"}).find("a")['href']

            pdf_share = None
            date_obj = None

            if pdf_link != "N/A" and not pdf_link.startswith("http"):
                pdf_share = f"https://home.odisha.gov.in{pdf_link}"

            if date_str != "N/A":
                date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()


            today = datetime.now().date() 

            if date_obj != today:
                continue
            else :
                annocuements.append({
                    "title": title,
                    "date": date_str,
                    "pdf_link": pdf_share
                })

        return annocuements
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
    
























































    


        