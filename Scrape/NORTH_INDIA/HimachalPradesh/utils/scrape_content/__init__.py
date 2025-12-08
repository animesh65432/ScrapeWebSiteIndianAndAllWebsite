from config.http import get_agent
from bs4 import BeautifulSoup
import re
from config.create_driver import create_driver
from utils.load_with_retry import load_with_retry
from config.safe_quit import safe_quit
import asyncio


async def scrape_content(url):
    driver = None
    try:
        driver = await create_driver()

        if not await load_with_retry(driver, url,html_element="b.NewsTitleHeading",retries=3, delay=3,isScraperAPIUsed=True):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            driver = None
            return None
        
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)
        await safe_quit(driver=driver)
        driver = None

        soup = BeautifulSoup(html, "html.parser")
        
        # Extract metadata
        title = extract_title(soup)
        press_number, date = extract_press_info(soup)
        
        # Extract main content
        content_paragraphs = extract_content(soup)
        
        # Convert to markdown
        markdown = create_markdown(title, press_number, date, content_paragraphs)
        
        return markdown

    except Exception as e:
        print(f"Content scraping error: {e}")
        await safe_quit(driver=driver)
        driver = None
        return None


def extract_title(soup):
    """Extract the press release title"""
    title_elem = soup.select_one("b.NewsTitleHeading")
    if title_elem:
        return title_elem.get_text(strip=True)
    
    # Fallback to h3 title
    h3_elem = soup.select_one("h3 b.NewsTitleHeading")
    if h3_elem:
        return h3_elem.get_text(strip=True)
    
    return "Press Release"


def extract_press_info(soup):
    """Extract press release number and date"""
    info_p = soup.select_one("p[align='left']")
    press_number = ""
    date = ""
    
    if info_p:
        text = info_p.get_text()
        # Extract number (e.g., "No. 1321/2025")
        number_match = re.search(r'No\.\s*(\d+/\d+)', text)
        if number_match:
            press_number = number_match.group(1)
        
        # Extract date
        date_match = re.search(r'(\d+(?:st|nd|rd|th)?\s+\w+\s+\d{4})', text)
        if date_match:
            date = date_match.group(1)
    
    return press_number, date


def extract_image(soup):
    """Extract main image URL"""
    img = soup.select_one("span.descpara img, a[onclick*='hs.expand'] img")
    if img and img.get('src'):
        return img['src']
    return None


def extract_content(soup):
    """Extract all content paragraphs"""
    content_paragraphs = []
    
    # Get all paragraphs inside span.descpara
    descpara = soup.select_one("span.descpara")
    if descpara:
        for p in descpara.find_all('p', recursive=True):
            text = p.get_text(strip=True)
            
            # Skip empty paragraphs, separators, and non-breaking spaces
            if not text or text in ['-0-', '\xa0', '']:
                continue
            
            # Skip if paragraph only contains whitespace
            if not text.strip():
                continue
            
            content_paragraphs.append(text)
    
    return content_paragraphs


def create_markdown(title, press_number, date, content_paragraphs):
    """Create formatted markdown from extracted content"""
    md_lines = []
    
    # Add title
    md_lines.append(f"# {title}")
    md_lines.append("")
    
    # Add metadata
    if press_number:
        md_lines.append(f"**Press Release No:** {press_number}")
    if date:
        md_lines.append(f"**Date:** {date}")
    
    if press_number or date:
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

    
    # Add content paragraphs
    for para in content_paragraphs:
        # Check if it's a subheading (shorter text, often in bold format)
        if len(para) < 100 and not para.endswith('.'):
            md_lines.append(f"## {para}")
        else:
            md_lines.append(para)
        
        md_lines.append("")
    
    # Join and clean up
    markdown = '\n'.join(md_lines).strip()
    
    # Remove excessive blank lines (more than 2 consecutive)
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    
    return markdown

