from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from bs4 import BeautifulSoup
from .convert_to_markdown import convert_to_markdown

def scrape_content(url):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        driver.quit()

        content_div = soup.find("div",{"id" :"row-content"})

        if not content_div:
            print("Content div not found")
            return None

        md_content = convert_to_markdown(content_div)
        
        return md_content

    except Exception as e:
        print("scrape_content error:", e)
        return None