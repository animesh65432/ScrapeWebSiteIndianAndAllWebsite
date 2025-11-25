from config.http import get_agent
from bs4 import BeautifulSoup
def scrape_content(url):
    try:
        session = get_agent(url)
        response = session.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        content_paragraphs = []

        # Extract paragraphs inside span.descpara
        for p in soup.select("span.descpara p"):
            text = p.get_text(strip=True)
            if text and text != "-0-" and text != "\xa0":
                content_paragraphs.append(text)

        content = "\n\n".join(content_paragraphs)
        return content

    except Exception as e:
        print(f"Content scraping error: {e}")
        return None