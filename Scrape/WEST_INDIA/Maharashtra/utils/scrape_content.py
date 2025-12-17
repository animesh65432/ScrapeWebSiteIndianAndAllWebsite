from config.create_driver import create_driver
from bs4 import BeautifulSoup
from utils.load_with_retry import load_with_retry
from config.safe_quit import safe_quit
import asyncio

async def scrape_content(url: str):
    driver = None
    try:
        driver = await create_driver(use_scraperapi=True)
        
        if not await load_with_retry(driver, url,html_element="div", retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            driver = None
            return None
        

        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None
        
        soup = BeautifulSoup(html, "html.parser")
        
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
        await safe_quit(driver=driver)
        return None
    
   