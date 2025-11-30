from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config.http import get_agent
from .scrape_content import scrape_content
from datetime import datetime, timedelta

def scrape_website(url):
    try:
        session = get_agent(url)
        response = session.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        announcements = []

        # Loop through each news item
        for li in soup.select("#lcp_instance_0 li"):
            a_tag = li.find("a")
            title = a_tag.get_text(strip=True) if a_tag else ""
            link = urljoin(url, a_tag['href']) if a_tag and a_tag.has_attr('href') else ""

            # Remove anchor text from li to get date text
            li_copy = BeautifulSoup(str(li), "html.parser")
            for a in li_copy.find_all("a"):
                a.extract()
            date_text = li_copy.get_text(strip=True)

            date_obj = datetime.strptime(date_text, "%B %d, %Y").date()
            
            today = datetime.today().date()

            if today == date_obj and link and title:
                announcements.append({
                    "title": title,
                    "link": link,
                    "content": scrape_content(link),
                    "state" :"Goa"
                })

        return announcements

    except Exception as e:
        print(f"Scraping Error: {e}")
        return None