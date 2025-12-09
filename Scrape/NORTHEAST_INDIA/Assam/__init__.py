from .utils import scrape_website
from config import NORTHEAST_INDIA
async def GetAssamAnnoucements():
    try :
        print("Scraping Assam Announcements...")
        return await scrape_website(NORTHEAST_INDIA["Assam"])
    except Exception as e:
        print("error in  Assam Announcements",e)
        return []