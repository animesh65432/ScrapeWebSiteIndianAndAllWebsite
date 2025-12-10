from config.create_driver import create_driver
from utils.load_with_retry import load_with_retry
from config.safe_quit import safe_quit
from bs4 import BeautifulSoup
from datetime import datetime
import asyncio

async def scapre_website(url:str):
    driver = None
    try:
        driver = await create_driver()

        if not await load_with_retry(driver, url,html_element=".notifications-view",part="northeast_india" ,retries=3, delay=3,):
            print("❌ Page failed to load after 3 retries")
            await safe_quit(driver=driver)
            return []
        
        loop = asyncio.get_event_loop()
        html = await loop.run_in_executor(None, lambda: driver.page_source)

        await safe_quit(driver=driver)
        driver = None
        
        soup = BeautifulSoup(html, 'html.parser')


        notification_div = soup.find("div", {"class": "notifications-view page-content-view border-content"})

        view_content = notification_div.find("div",{"class" : "view-content"})

        item_list = view_content.find("div" ,{"class" :"item-list"})
        
        annoucements_lists = item_list.find("ul").find_all("li")

        annoucements = []


        for annoucement in annoucements_lists :
            date_html = annoucement.find("span",{"class" :"views-field views-field-field-date1 field-color"}).find("small").get_text(strip=True)
            date_str = date_html.split(":")[1].strip()
            date_obj = datetime.strptime(date_str, "%d %b %Y")

            today = datetime.today().date()
            date_only = date_obj.date()

            if today != date_only:
                continue

            title = annoucement.find("span",{"class" :"views-field views-field-title"}).find("span",{"class" : "field-content"}).find("a").get_text(strip=True)
            pdf_link = annoucement.find("span" , {"class" : "field-content field-color"}).find("a")["href"]


            annoucements.append({
                "title" : title,
                "pdf_link" : pdf_link,
                "state" :"Meghalaya"
            })

        return annoucements
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        await safe_quit(driver=driver)
        return []