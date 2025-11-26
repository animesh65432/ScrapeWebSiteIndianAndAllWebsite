from bs4 import BeautifulSoup
from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver

def scrape_website(url:str):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        html = driver.page_source

        driver.quit()

        soup = BeautifulSoup(html, "html.parser")

        print(soup)

        return None
    except Exception as e:
        print("scrape_website_utils",e)
        return None