from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from typing import List, Dict

def scraping_website(url: str, base_url: str = None) -> List[Dict[str, str]]:
    """
    Scrapes J&K government notifications table.
    
    Args:
        url: The URL to scrape
        base_url: Base URL for resolving relative PDF links (optional)
    
    Returns:
        List of dictionaries containing notification data
    """
    try:
        # Create session with headers
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        response = session.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find the table - it's inside section with id="tables"
        table_section = soup.find("section", id="tables")
        if not table_section:
            print("Table section not found")
            return []
        
        # Find the table within the section
        table = table_section.find("table")
        if not table:
            print("Table not found")
            return []
        
        notifications = []
        
        # Find all rows (skip header row)
        rows = table.find("tbody").find_all("tr")[1:]  # Skip first row (header)
        
        for row in rows:
            cols = row.find_all("td")
            
            if len(cols) >= 3:
                date = cols[0].get_text(strip=True)
                order_no = cols[1].get_text(strip=True)
                
                # Extract subject and PDF link
                subject_cell = cols[2]
                link_tag = subject_cell.find("a")
                
                if link_tag:
                    subject = link_tag.get_text(strip=True)
                    pdf_link = link_tag.get("href", "")
                    
                    # Resolve relative URLs
                    if base_url and pdf_link:
                        pdf_link = urljoin(base_url, pdf_link)
                else:
                    subject = subject_cell.get_text(strip=True)
                    pdf_link = ""
                
                notification = {
                    "date": date,
                    "order_number": order_no,
                    "subject": subject,
                    "pdf_link": pdf_link
                }
                
                notifications.append(notification)
        
        return notifications

    except requests.RequestException as e:
        print(f"Request error: {e}")
        return []
    except Exception as e:
        print(f"Scraping error: {e}")
        return []

