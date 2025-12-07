from config.create_driver import create_driver
from  utils.load_with_retry import load_with_retry
from bs4 import BeautifulSoup
from datetime import datetime 
from config.safe_quit import safe_quit
import asyncio

async def scarpe_website(url):
    driver = None
    try :
        driver = await create_driver()

        if not await load_with_retry(driver, url, html_element="table",retries=3, delay=3):
            print("❌ Page failed to load after 3 retries")
            safe_quit(driver=driver)
            return []
        
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None

        soup = BeautifulSoup(html, 'html.parser')


        table = soup.find("table",{"class" :"table table-borderd table-striped paginationtbl"})

        annoucements_htmllist = table.find("tbody").find_all("tr")

        announcements = []

        for annoucement in annoucements_htmllist :
            title = annoucement.find("a").getText(strip=True)
            link = annoucement.find("a")['href']
            date_str = annoucement.find_all("td")[2].getText(strip=True)

            date_obj = datetime.strptime(date_str, "%d/%b/%Y")
            today = datetime.today()


            if date_obj.date() == today.date() :
                announcements.append({
                    "title" : title,
                    "pdf_link"  : f"https://information.up.gov.in{link}",
                    "state" : "UttarPradesh"
                })

        return announcements
    
    except Exception as e :
        print("scarpe_website",e)
        await safe_quit(driver=driver)
        return []