from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime 

def scarpe_website(url):
    try :
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(120)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        driver.quit()

        table = soup.find("table",{"class" :"table table-borderd table-striped paginationtbl"})

        annoucements_htmllist = table.find("tbody").find_all("tr")

        announcements = []

        for annoucement in annoucements_htmllist :
            title = annoucement.find("a").getText(strip=True)
            link = annoucement.find("a")['href']
            date_str = annoucement.find_all("td")[2].getText(strip=True)

            date_obj = datetime.strptime(date_str, "%d/%b/%Y")
            today = datetime.today()


            if date_obj.date() == today.date() :
                announcements.append({
                    "title" : title,
                    "pdf_link"  : f"https://information.up.gov.in{link}",
                    "state" : "UttarPradesh"
                })

        return announcements
    
    except Exception as e :
        print("scarpe_website",e)
        return None