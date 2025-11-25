from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config.http import get_agent
from .scrape_content import scrape_content

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
            date = spans[-1].get_text(strip=True) if len(spans) > 1 else ""

            announcements.append({
                "title": title,
                "link": link,
                "date": date,
                "content": scrape_content(link) if link else None
            })

        return announcements

    except Exception as e:
        print(f"Scraping error: {e}")
        return []
