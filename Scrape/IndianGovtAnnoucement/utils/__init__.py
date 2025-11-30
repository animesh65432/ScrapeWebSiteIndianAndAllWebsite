from urllib.parse import urljoin
from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from bs4 import BeautifulSoup
from .scrape_content import scrape_content

def scrape_website(url:str,base_url:str="https://www.pib.gov.in/Allrel.aspx"):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        announcements = []
        
        office_sections = soup.find_all("li")

        for section in office_sections:
            office_name_tag = section.find("h3", class_="font104")
            release_list = section.find("ul", class_="num")
            
            if not office_name_tag or not release_list:
                continue
            
            announcement_type = office_name_tag.get_text(strip=True)
            
            for li in release_list.find_all("li"):
                link_elem = li.find("a")
                
                if not link_elem:
                    continue
                
                title = link_elem.get("title") or link_elem.get_text(strip=True)
                
                href = link_elem.get("href")
                
                if href:
                    href = urljoin(base_url, href)
                
                content = None
                
                if not href:
                    continue
                else :
                    content = scrape_content(href)
                    
                announcements.append({
                    "department": announcement_type,
                    "title": title.strip(),
                    "link": href,
                    "content": content,
                    "state": "IndianGovtAnnouncement"
                })
        
        return announcements
    
    except Exception as e:
        print("scrape_website", e)
        return None