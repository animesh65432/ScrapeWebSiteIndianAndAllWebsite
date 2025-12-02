from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config.chromeOptions import Get_Chrome_Options
from .scrape_content import scrape_content
from datetime import datetime
from selenium import webdriver

def scraping_website(url):
    try:
        chromeOptions = Get_Chrome_Options(url)
        driver = webdriver.Chrome(options=chromeOptions)
        driver.get(url)

        html = driver.page_source

        soup = BeautifulSoup(html, "html.parser")

        driver.quit()
        
        announcements = []

        for li in soup.select("li.modren"):
            a_tag = li.find("a")
            link = urljoin(url, a_tag['href']) if a_tag and a_tag.has_attr('href') else ""
            
            spans = li.find_all("span")
            title = spans[0].get_text(strip=True) if len(spans) > 0 else ""
            date_str = spans[-1].get_text(strip=True) if len(spans) > 1 else ""

            date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
            
            today = datetime.today().date()


            if today == date_obj and link and title:
                announcements.append({
                    "title": title,
                    "link": link,
                    "content": scrape_content(link) ,
                    "state" :"HimachalPradesh"
                })


        return announcements

    except Exception as e:
        print(f"Scraping error: {e}")
        return []
