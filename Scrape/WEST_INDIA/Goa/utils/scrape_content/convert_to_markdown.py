import re
def convert_to_markdown(title, date, categories, content_div):
    """Convert scraped content to Markdown format"""
    md_lines = []
    
    # Add title as H1
    if title:
        md_lines.append(f"# {title}")
        md_lines.append("")
    
    # Add metadata
    if date:
        md_lines.append(f"**Date:** {date}")
        md_lines.append("")
    
    if categories:
        md_lines.append(f"**Categories:** {', '.join(categories)}")
        md_lines.append("")
    
    md_lines.append("---")
    md_lines.append("")
    
    # Process content paragraphs
    paragraphs = content_div.find_all(['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'ul', 'ol'])
    
    for elem in paragraphs:
        text = elem.get_text(strip=True)
        
        if not text or len(text) < 2:
            continue
        
        # Skip reference codes (like DI/INF/...)
        if re.match(r'^[A-Z]{2}/[A-Z]+/.*\d+$', text):
            md_lines.append(f"*{text}*")
            md_lines.append("")
            continue
        
        # Handle headings
        if elem.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(elem.name[1]) + 1  # Shift down since title is H1
            md_lines.append(f"{'#' * level} {text}")
            md_lines.append("")
        
        # Handle list items
        elif elem.name == 'li':
            md_lines.append(f"- {text}")
        
        # Handle paragraphs
        elif elem.name == 'p':
            # Check if it's a location/date line (like "Panaji : December 01, 2025")
            if re.match(r'^[A-Za-z\s]+\s*:\s*[A-Z][a-z]+\s+\d{1,2},\s*\d{4}', text):
                md_lines.append(f"**{text}**")
                md_lines.append("")
            else:
                md_lines.append(text)
                md_lines.append("")
    
    # Join and clean up
    markdown = '\n'.join(md_lines).strip()
    
    # Remove excessive blank lines (more than 2 consecutive)
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    
    return markdown
