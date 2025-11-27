from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from bs4 import BeautifulSoup

def scrape_content(url: str):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        # Find the main content div
        content_div = soup.find("div", {"class": "post-content"})

        # Extract text from <p> tags only, ignoring other divs/icons
        paragraphs = content_div.find_all("p")
        text_content = "\n\n".join([p.get_text(strip=True) for p in paragraphs])

        print(text_content)
        return text_content

    except Exception as e:
        return f"An error occurred in scrape_content: {str(e)}"
