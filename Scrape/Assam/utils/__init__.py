from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def scrape_website(url: str):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, "html.parser")

        announcements = []

        # Correct base URL
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        for doc in soup.select(".documents"):
            title_element = doc.select_one(".documents_title a")
            if not title_element:
                continue
            title = title_element.get_text(strip=True)
            pdf_link = title_element.get("href", "")

            time_element = doc.select_one(".documents_date time")
            date = time_element.get_text(strip=True) if time_element else ""

            if title and pdf_link:
                full_pdf_url = pdf_link if pdf_link.startswith("http") else urljoin(base_url, pdf_link)
                announcements.append({
                    "title": title,
                    "date": date,
                    "source": full_pdf_url
                })

        return announcements

    except Exception as e:
        print("Scraping Error:", str(e))
        return []
