from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scarpContent(url: str):
    driver = None
    try:
        options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(120)
        driver.get(url)

        wait = WebDriverWait(driver, 30)

        
        loader = (By.CSS_SELECTOR, "app-mini-loader .mini-loading")
        wait.until(EC.invisibility_of_element_located(loader))

        soup = BeautifulSoup(driver.page_source, "html.parser")

     
        content_divs = soup.select("div.press-release-details-left p div")

        content = "\n".join(
            d.get_text(strip=True)
            for d in content_divs
            if d.get_text(strip=True)
        )

        return content

    except Exception as e:
        return f"Error: {e}"

    finally:
        if driver:
            driver.quit()
