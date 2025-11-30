from bs4 import BeautifulSoup
from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver

def scrape_content(url:str):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        main_container = soup.find("div", class_="innner-page-main-about-us-content-right-part")

        if not main_container:
            print(f"Main container not found for {url}")
            return None

        paragraphs = main_container.find_all("p")

        content = " ".join(
            p.get_text(" ", strip=True) for p in paragraphs if p.get_text(strip=True)
        )


        return content 
    
    except Exception as e:
        print("scrape_content", e)
        return ""