from config.create_driver import create_driver
from bs4 import BeautifulSoup
from datetime import datetime 
from utils.load_with_retry import load_with_retry
from  config.safe_quit import safe_quit
import asyncio

async def scrape_website(url: str) -> list:
    driver = None
    try:
        driver = await create_driver()
        
        if not await load_with_retry(driver ,url, html_element="table",part="northeast_india",retries=3, delay=3,isScraperAPIUsed=True):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            driver = None
            return []
      
        
        loop = asyncio.get_event_loop()

        html = await loop.run_in_executor(None, lambda: driver.page_source)
        

        soup = BeautifulSoup(html, "html.parser")
        
        await safe_quit(driver=driver)
        driver = None
        # Find all table rows in tbody

        Annoucements = []

        table = soup.select_one(".table-container table tbody")

        
        if table:
            rows = table.find_all("tr")
            
            for row in rows:
                cols = row.find_all("td")
                
                if len(cols) >= 4:
                    title = cols[1].get_text(strip=True)
                    date_str = cols[2].get_text(strip=True)
                    
                    # Extract PDF link
                    link_tag = cols[3].find("a")
                    pdf_link = link_tag.get("href", "") if link_tag else ""

                    date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
                    
                    today = datetime.today().date()


                    if date_obj == today:
                        notice_data = {
                            "title": title,
                            "pdf_link":f"https://arunachalpradesh.gov.in/{pdf_link}",
                            "state" :"ArunachalPradesh"
                        }
                        Annoucements.append(notice_data)
        
        return Annoucements

    except Exception as e:
        print(f"Error: {e}")
        await safe_quit(driver=driver)
        driver = None
        return []


















