from selenium import webdriver
from bs4 import BeautifulSoup
from config.chromeOptions import Get_Chrome_Options

def scrape_content(url: str):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        driver.quit()

        # Find the main container
        detail = soup.select_one(".detail-inner")
        if not detail:
            print("No detail-inner found")
            return None

      
        paragraphs = []
        for p in detail.find_all("p"):
            text = p.get_text(strip=True)
            
           
            if not text:
                continue

            # skip last updated <p>
            if p.get("class") == ["float-right"]:
                continue

            paragraphs.append(text)

        # Join content cleanly
        full_content = "\n\n".join(paragraphs)

        return full_content

    except Exception as e:
        print(f"Error scraping website: {e}")
        return None
