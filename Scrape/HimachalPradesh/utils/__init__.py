from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config.http import get_agent
from .scrape_content import scrape_content
from datetime import datetime, timedelta

def scraping_website(url):
    try:
        session = get_agent(url)
        response = session.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        announcements = []

        for li in soup.select("li.modren"):
            a_tag = li.find("a")
            link = urljoin(url, a_tag['href']) if a_tag and a_tag.has_attr('href') else ""
            
            spans = li.find_all("span")
            title = spans[0].get_text(strip=True) if len(spans) > 0 else ""
            date_str = spans[-1].get_text(strip=True) if len(spans) > 1 else ""

            date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
            
            today = datetime.today().date()

            if link and title and today == date_obj:
                announcements.append({
                    "title": title,
                    "link": link,
                    "content": scrape_content(link) 
                })

        return announcements

    except Exception as e:
        print(f"Scraping error: {e}")
        return []
