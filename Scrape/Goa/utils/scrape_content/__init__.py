from config.http import get_agent
from bs4 import BeautifulSoup
from .convert_to_markdown import convert_to_markdown


def scrape_content(url):
    try:
        session = get_agent(url)
        response = session.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title
        title = ""
        title_elem = soup.select_one(".cm-entry-title, h1.entry-title, .entry-title")
        if title_elem:
            title = title_elem.get_text(strip=True)

        # Extract date
        date = ""
        date_elem = soup.select_one("time.entry-date, .cm-post-date time")
        if date_elem:
            date = date_elem.get_text(strip=True)

        # Extract categories
        categories = []
        category_links = soup.select(".cm-post-categories a")
        categories = [cat.get_text(strip=True) for cat in category_links]

        # Get main content
        content_div = soup.select_one(".cm-entry-summary") or soup.select_one(".entry-content")
        
        if not content_div:
            print("Content div not found")
            return None

        # Convert to markdown
        markdown = convert_to_markdown(title, date, categories, content_div)
        
        return markdown

    except Exception as e:
        print(f"Error fetching content: {e}")
        return None
