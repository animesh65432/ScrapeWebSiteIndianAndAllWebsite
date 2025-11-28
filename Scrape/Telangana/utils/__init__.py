from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from .scrape_content import scrape_content

def scrape_website(url: str):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, "html.parser")

        # Best, reliable selector
        articleLists = soup.find_all("article", class_="elementor-post")

        announcements = []
        today = (datetime.today() - timedelta(days=2)).date()

        for article in articleLists:
            link = article.find("a")["href"]

            title = (
                article.find("h3", class_="elementor-post__title")
                .find("a")
                .get_text(strip=True)
            )

            date_str = article.find("span", class_="elementor-post-date").get_text(strip=True)

            # Convert to datetime
            try:
                parsed_date = datetime.strptime(date_str, "%B %d, %Y").date()
            except:
                continue

            # Check date match
            if parsed_date == today:
                announcements.append({
                    "title": title,
                    "link": link
                })

        # If no announcements for today
        if not announcements:
            return []

        # Process only first match
        for announcement in announcements:
            content = scrape_content(announcement["link"])
            announcement["content"] = content

        return announcements

    except Exception as e:
        return f"scrape_website error occurred: {str(e)}"
