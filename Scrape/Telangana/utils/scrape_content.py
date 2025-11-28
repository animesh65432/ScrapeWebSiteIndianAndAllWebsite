from bs4 import BeautifulSoup
from selenium import webdriver
from config.chromeOptions import Get_Chrome_Options

def scrape_content(url):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract ONLY content
        content_div = soup.find("div", class_="entry-content")
        content = content_div.get_text("\n", strip=True) if content_div else ""

        driver.quit()

        return content

    except Exception as e:
        return f"scrape_telangana_content error occurred: {str(e)}"
