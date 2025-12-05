from selenium import webdriver
from config.chromeOptions import Get_Chrome_Options
from bs4 import BeautifulSoup
import time

def scrape_content(url: str):
    driver = None
    print(f"Scraping content from: {url}")
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(120)
        driver.get(url)
        
        time.sleep(3)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        
        # Find the main content container
        news_details = soup.find("p", {"id": "newsdetails"})
        
        if not news_details:
            print("Content not found")
            return None
        
        # Initialize markdown content
        markdown_content = []
        
        # Extract title
        title = soup.find("h3", {"id": "lblNewsTitle"})
        if title:
            markdown_content.append(f"# {title.get_text(strip=True)}\n")
        
        # Extract subtitle
        subtitle = soup.find("p", {"id": "lblSubNewsTitle"})
        if subtitle:
            subtitle_text = subtitle.get_text(strip=True)
            markdown_content.append(f"*{subtitle_text}*\n")
        
        # Extract date
        date = soup.find("p", {"id": "lblLocPDtUTm"})
        if date:
            markdown_content.append(f"**{date.get_text(strip=True)}**\n")
        
        markdown_content.append("---\n")
        
        # Extract all paragraphs and format them
        for element in news_details.children:
            if element.name == "p":
                text = element.get_text(strip=True)
                if text:
                    # Check if it's a bold heading
                    bold_tag = element.find("b")
                    if bold_tag and len(element.get_text(strip=True)) < 100:
                        markdown_content.append(f"\n## {text}\n")
                    else:
                        markdown_content.append(f"{text}\n")
        
        # Extract reporter name
        reporter = soup.find("label", {"id": "lblRepName"})
        if reporter:
            markdown_content.append(f"\n---\n*Reporter: {reporter.get_text(strip=True)}*")
        
        # Join all content
        final_content = "\n".join(markdown_content)
        
        # Clean up extra blank lines
        final_content = "\n".join([line for line in final_content.split("\n") if line.strip() or line == ""])
        
        return final_content
        
    except Exception as e:
        print("Error in scrape_content:", e)
        if driver:
            driver.quit()
        return None