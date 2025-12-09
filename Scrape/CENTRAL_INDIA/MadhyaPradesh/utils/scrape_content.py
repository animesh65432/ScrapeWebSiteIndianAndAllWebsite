from config.create_driver import create_driver
from bs4 import BeautifulSoup
from  utils.load_with_retry import load_with_retry
from config.safe_quit import safe_quit
import asyncio

async def scrape_content(url: str):
    driver = None
    try:
        driver = await create_driver()
        
        if not await load_with_retry(driver, url,html_element="#newsdetails", part="central_India",retries=3, delay=3,isScraperAPIUsed=True):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return None
    

        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)

        soup = BeautifulSoup(html, 'html.parser')
        
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
        await safe_quit(driver=driver)
        return None