from config.chromeOptions import Get_Chrome_Options
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def scrape_content(url: str):
    driver = None
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        
        driver.get(url)
        
        # Wait for main content to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "main"))
        )
        
        soup = BeautifulSoup(driver.page_source, "html.parser")

        driver.quit()
        
        # Extract meaningful content
        content = {}
        
        # Get title
        title = soup.find('h1')
        content['title'] = title.get_text(strip=True) if title else ""
        
        # Get publish date
        meta_info = soup.find('div', class_='meta-info')
        if meta_info:
            content['publish_date'] = meta_info.get_text(strip=True)
        
        # Get main content
        main_content = soup.find('div', id='row-content')
        if main_content:
            # Extract all paragraphs
            paragraphs = main_content.find_all('p')
            content['body'] = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
        
        # Get breadcrumb for context
        breadcrumb = soup.find('nav', {'aria-label': 'Breadcrumb'})
        if breadcrumb:
            crumbs = [li.get_text(strip=True) for li in breadcrumb.find_all('li')]
            content['breadcrumb'] = ' > '.join(crumbs)
        
        # Convert to markdown
        markdown = f"# {content.get('title', '')}\n\n"
        
        if 'publish_date' in content:
            markdown += f"**{content['publish_date']}**\n\n"
        
        markdown += "---\n\n"
        
        if 'body' in content:
            markdown += content['body']
        
        if 'breadcrumb' in content:
            markdown += f"\n\n---\n\n**Navigation:** {content['breadcrumb']}"
        
        return markdown
        
    except Exception as e:
        print(f"Error in scrape_content: {e}")
        return None
    
   