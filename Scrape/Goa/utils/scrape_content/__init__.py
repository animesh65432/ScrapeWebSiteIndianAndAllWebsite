from config.http import get_agent
from bs4 import BeautifulSoup

def scrape_content(url):
    try:
        session = get_agent(url)
        response = session.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Try to get .cm-entry-summary first, else .entry-content
        content_div = soup.select_one(".cm-entry-summary") or soup.select_one(".entry-content")
        text_content = ""
        if content_div:
            text_content = content_div.get_text(separator=" ", strip=True)
        
        return ' '.join(text_content.split())  # Replace multiple spaces with single space

    except Exception as e:
        print(f"Error fetching content: {e}")
        return None