from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re

def scrape_content(url: str):
    driver = None
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        # Wait for content to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "post-content"))
        )
        
        # FIX: Get the page source BEFORE quitting the driver
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Find the main content div
        content_div = soup.find("div", {"class": "post-content"})
        
        if not content_div:
            return "Content not found"
        
        # Initialize markdown content
        markdown = ""
        
        # Extract all paragraphs
        paragraphs = content_div.find_all("p")
        
        for i, p in enumerate(paragraphs):
            text = p.get_text(strip=True)
            
            if not text:
                continue
            
            # Check if it's a reference number (first paragraph)
            if i == 0 and re.match(r'^\d+/\d+-\d+$', text):
                markdown += f"**Reference:** {text}\n\n"
                continue
            
            # Check if it starts with "Dated" (second paragraph - header)
            if text.startswith("Dated"):
                markdown += f"**{text}**\n\n"
                continue
            
            # Check for bold text (strong tags)
            strong_tags = p.find_all("strong")
            if strong_tags:
                # Replace strong tags with markdown bold
                for strong in strong_tags:
                    strong_text = strong.get_text(strip=True)
                    text = text.replace(strong_text, f"**{strong_text}**")
            
            # Add paragraph to markdown
            markdown += f"{text}\n\n"
    
        
        return markdown.strip()
        
    except Exception as e:
        return f"An error occurred in scrape_content: {str(e)}"
    
    finally:
        # FIX: Always quit the driver, even if errors occur
        if driver:
            driver.quit()