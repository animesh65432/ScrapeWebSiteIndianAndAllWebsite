from bs4 import BeautifulSoup
from config.create_driver import create_driver
import re
from utils.load_with_retry import load_with_retry
from config.safe_quit import safe_quit
import asyncio

async def scrape_content(url: str):
    driver = None
    try:
        driver = await create_driver()
        
        if not load_with_retry(driver, url, retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return None
        
        
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.get(url))

        await safe_quit(driver=driver)
        driver = None

        soup = BeautifulSoup(html, "html.parser")
    
        # Find the main detail container
        detail = soup.select_one(".detail-inner")
        
        if not detail:
            print("No detail-inner found")
            return None
        

        # Extract all components
        title = extract_title(detail)
        date = extract_date(detail)
        images = extract_images(detail)
        paragraphs = extract_paragraphs(detail)
        
        # Create markdown
        markdown = create_markdown(title, date, images, paragraphs)
        
        return markdown

    except Exception as e:
        print(f"Error scraping website: {e}")
        await safe_quit(driver=driver)
        return None


def extract_title(detail):
    """Extract the news title"""
    # Try h2 first, then h1
    title_elem = detail.find("h2") or detail.find("h1")
    if title_elem:
        return title_elem.get_text(strip=True)
    return ""


def extract_date(detail):
    """Extract the publication date"""
    # Look for date in various formats
    date_elem = detail.find("p", class_="float-right")
    if date_elem:
        text = date_elem.get_text(strip=True)
        # Extract date if it contains common date patterns
        if any(keyword in text.lower() for keyword in ['last updated', 'updated', 'പുതുക്കിയത്', 'date']):
            return text
    
    # Alternative: look for date in span or other elements
    for elem in detail.find_all(['span', 'p', 'div']):
        text = elem.get_text(strip=True)
        # Match date patterns (DD/MM/YYYY or similar)
        if re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{4}', text):
            return text
    
    return ""


def extract_images(detail):
    """Extract all images from the content"""
    images = []
    
    for img in detail.find_all("img"):
        src = img.get('src', '')
        alt = img.get('alt', '')
        
        # Skip small images, icons, logos
        if any(skip in src.lower() for skip in ['logo', 'icon', 'banner']):
            continue
        
        # Make sure it's a full URL
        if src and (src.startswith('http') or src.startswith('/')):
            if src.startswith('/'):
                src = f"https://kerala.gov.in{src}"
            images.append({'src': src, 'alt': alt})
    
    return images


def extract_paragraphs(detail):
    """Extract all content paragraphs"""
    paragraphs = []
    
    # Get all p tags
    for p in detail.find_all("p"):
        # Skip date/update info
        if p.get("class") and "float-right" in p.get("class"):
            continue
        
        text = p.get_text(strip=True)
        
        # Skip empty paragraphs
        if not text:
            continue
        
        # Skip if it's just a date pattern
        if re.match(r'^(Last Updated|Updated|പുതുക്കിയത്).*\d{1,2}[/-]\d{1,2}[/-]\d{4}', text, re.IGNORECASE):
            continue
        
        paragraphs.append(text)
    
    # Also check for content in div tags if paragraphs are few
    if len(paragraphs) < 2:
        for div in detail.find_all("div", class_=["content", "news-content", "detail-content"]):
            text = div.get_text(strip=True)
            if text and len(text) > 50:
                # Split by double line breaks if it's a large block
                parts = re.split(r'\n\s*\n', text)
                paragraphs.extend([p.strip() for p in parts if p.strip()])
    
    return paragraphs


def create_markdown(title, date, images, paragraphs):
    """Create formatted markdown from extracted content"""
    md_lines = []
    
    # Add title
    if title:
        md_lines.append(f"# {title}")
        md_lines.append("")
    
    # Add date
    if date:
        md_lines.append(f"**{date}**")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
    
    # Add content with images
    img_index = 0
    for i, para in enumerate(paragraphs):
        md_lines.append(para)
        md_lines.append("")
        
        # Insert first image after 2nd paragraph
        if i == 1 and img_index < len(images):
            img = images[img_index]
            alt_text = img['alt'] if img['alt'] else "News Image"
            md_lines.append(f"![{alt_text}]({img['src']})")
            md_lines.append("")
            img_index += 1
    
    # Add remaining images at the end
    while img_index < len(images):
        img = images[img_index]
        alt_text = img['alt'] if img['alt'] else "News Image"
        md_lines.append(f"![{alt_text}]({img['src']})")
        md_lines.append("")
        img_index += 1
    
    # Join and clean up
    markdown = '\n'.join(md_lines).strip()
    
    # Remove excessive blank lines
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    
    return markdown

def clean_text(text):
    """Clean text"""
    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)
    # Remove spaces before punctuation
    text = re.sub(r'\s+([,.;:!?])', r'\1', text)
    return text

