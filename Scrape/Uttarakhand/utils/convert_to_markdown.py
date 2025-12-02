import re

def convert_to_markdown(content_div):
    md_lines = []
    
    # Extract title/date if present
    date_elem = content_div.find(string=re.compile(r'\d{2}-\d{2}-\d{4}'))
    if date_elem:
        md_lines.append(f"**Date:** {date_elem.strip()}")
        md_lines.append("")
    
    # Extract publish date
    publish_date = content_div.find(string=re.compile(r'Publish Date'))
    if publish_date:
        md_lines.append(f"*{publish_date.strip()}*")
        md_lines.append("")
    
    # Process paragraphs
    for elem in content_div.find_all(['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        text = elem.get_text(strip=True)
        
        if not text:
            continue
            
        # Handle headings
        if elem.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(elem.name[1])
            md_lines.append(f"{'#' * level} {text}")
            md_lines.append("")
        
        # Handle paragraphs
        elif text and text not in ['', '0']:
            # Clean up multiple spaces
            text = re.sub(r'\s+', ' ', text)
            md_lines.append(text)
            md_lines.append("")
    
    # Join all lines
    markdown = '\n'.join(md_lines).strip()
    
    return markdown