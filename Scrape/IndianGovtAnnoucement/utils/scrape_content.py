from bs4 import BeautifulSoup
from config.chromeOptions import Get_Chrome_Options
from selenium import webdriver
import re
import time


def scrape_content(url: str):
    try:
        chrome_options = Get_Chrome_Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        # Wait for page to load
        time.sleep(2)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        main_container = soup.find("div", class_="innner-page-main-about-us-content-right-part")
        
        if not main_container:
            print(f"Main container not found for {url}")
            return None

        # Extract all components
        ministry = extract_ministry(main_container)
        title = extract_title(main_container)
        subtitle = extract_subtitle(main_container)
        date_time = extract_datetime(main_container)
        release_id = extract_release_id(main_container)
        images = extract_images(main_container)
        paragraphs = extract_paragraphs(main_container)
        
        # Create markdown
        markdown = create_markdown(
            ministry, title, subtitle, date_time, 
            release_id, images, paragraphs
        )
        
        return markdown
    
    except Exception as e:
        print("scrape_content error:", e)
        return None


def extract_ministry(container):
    """Extract ministry/department name"""
    ministry_elem = container.find("div", class_="MinistryNameSubhead")
    if ministry_elem:
        return ministry_elem.get_text(strip=True)
    return ""


def extract_title(container):
    """Extract main title"""
    title_elem = container.find("h2", id="Titleh2")
    if title_elem:
        return title_elem.get_text(strip=True)
    return ""


def extract_subtitle(container):
    """Extract subtitle"""
    subtitle_elem = container.find("h3", id="Subtitleh3")
    if subtitle_elem:
        span = subtitle_elem.find("span")
        if span:
            text = span.get_text(strip=True)
        else:
            text = subtitle_elem.get_text(strip=True)
        # Remove leading <br/> text
        text = re.sub(r'^<br\s*/?\s*>', '', text).strip()
        return text
    return ""


def extract_datetime(container):
    """Extract publish date and time"""
    datetime_elem = container.find("div", class_="ReleaseDateSubHeaddateTime")
    if datetime_elem:
        text = datetime_elem.get_text(strip=True)
        # Extract date and source
        match = re.search(r'(\d+\s+\w+\s+\d{4}\s+\d+:\d+\w+)\s+by\s+(.+)', text)
        if match:
            return f"{match.group(1)} | {match.group(2)}"
        # Handle Hindi format
        text = text.replace('प्रविष्टि तिथि:', '').strip()
        return text
    return ""


def extract_release_id(container):
    """Extract release ID"""
    release_elem = container.find("span", id="ReleaseId")
    if release_elem:
        text = release_elem.get_text(strip=True)
        match = re.search(r'(\d+)', text)
        if match:
            return match.group(1)
    return ""


def extract_images(container):
    """Extract all content images"""
    images = []
    
    # Find images in paragraphs with style text-align:center
    for p in container.find_all("p", style=lambda x: x and 'text-align:center' in x):
        for img in p.find_all("img"):
            src = img.get('src', '')
            alt = img.get('alt', '')
            
            # Skip logo/header images
            if 'azadi' in src.lower() or 'logo' in src.lower() or 'ph2021' in src:
                continue
            
            if src and src.startswith('http'):
                images.append({'src': src, 'alt': alt})
    
    return images


def extract_paragraphs(container):
    """Extract all content paragraphs"""
    paragraphs = []
    
    # Get all direct p tags
    for p in container.find_all("p", recursive=True):
        # Skip if inside center tag, blockquote, or twitter embed
        if (p.find_parent("center") or 
            p.find_parent("blockquote") or 
            p.find_parent(class_="twitter-tweet")):
            continue
        
        # Skip image-only paragraphs
        if p.find("img") and not p.get_text(strip=True):
            continue
        
        # Skip paragraphs with images that have text-align:center style
        if p.get('style') and 'text-align:center' in p.get('style'):
            # Check if it's only an image
            text = p.get_text(strip=True)
            if not text or (p.find("img") and len(text) < 10):
                continue
        
        text = p.get_text(strip=True)
        
        # Skip empty, markers, or author credits
        if not text or text in ['***', ' ', '  ']:
            continue
        
        # Skip author credit patterns
        if re.match(r'^[A-Z]{2}/[A-Z]{2}/[A-Z]{2}$', text):
            continue
        
        # Skip release ID
        if 'रिलीज़ आईडी' in text or 'Release ID' in text.lower():
            continue
        
        # Skip visitor count
        if 'आगंतुक पटल' in text or 'visitor' in text.lower():
            continue
        
        paragraphs.append(text)
    
    return paragraphs


def create_markdown(ministry, title, subtitle, date_time, release_id, images, paragraphs):
    """Create formatted markdown from extracted content"""
    md_lines = []
    
    # Add ministry
    if ministry:
        md_lines.append(f"**{ministry}**")
        md_lines.append("")
    
    # Add title
    if title:
        md_lines.append(f"# {title}")
        md_lines.append("")
    
    # Add subtitle
    if subtitle:
        md_lines.append(f"## {subtitle}")
        md_lines.append("")
    
    # Add metadata
    if date_time:
        md_lines.append(f"**प्रकाशन तिथि:** {date_time}")
    if release_id:
        md_lines.append(f"**रिलीज़ आईडी:** {release_id}")
    
    if date_time or release_id:
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
    
    # Add content with images
    img_inserted = 0
    for i, para in enumerate(paragraphs):
        md_lines.append(para)
        md_lines.append("")
        
        # Insert first image after 2nd paragraph
        if i == 1 and img_inserted < len(images):
            img = images[img_inserted]
            alt_text = img['alt'] if img['alt'] else "Press Release Image"
            md_lines.append(f"![{alt_text}]({img['src']})")
            md_lines.append("")
            img_inserted += 1
    
    # Add remaining images
    while img_inserted < len(images):
        img = images[img_inserted]
        alt_text = img['alt'] if img['alt'] else "Press Release Image"
        md_lines.append(f"![{alt_text}]({img['src']})")
        md_lines.append("")
        img_inserted += 1
    
    # Join and clean
    markdown = '\n'.join(md_lines).strip()
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    
    return markdown


def clean_text(text):
    """Clean text"""
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\s+([,.;:!?])', r'\1', text)
    return text

