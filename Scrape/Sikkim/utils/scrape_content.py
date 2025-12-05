
from bs4 import BeautifulSoup
from selenium import webdriver
from config.chromeOptions import Get_Chrome_Options

def scrape_content(url):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(120)
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find the main content card
        content_card = soup.find("div", class_="card-body")
        
        if content_card:
            content_div = content_card.find("div", style="text-align:justify")
            content_text = content_div.get_text(strip=True) if content_div else "No content found"
            
            return content_text.strip()
        else:
            return "Content not found"
            
    except Exception as e:
        return f"Error during scraping: {str(e)}"
    finally:
        driver.quit()