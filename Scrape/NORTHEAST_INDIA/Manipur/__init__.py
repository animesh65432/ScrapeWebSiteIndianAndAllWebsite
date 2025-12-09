from .utils import scrape_website
from config import NORTHEAST_INDIA

async def GetAllManipurAnnoucements():
    try :
        print("Scraping Manipur Announcements...")
        
        return await scrape_website(NORTHEAST_INDIA["Manipur"])
    except Exception as e :
        print("GetAllManipurAnnoucements",e)

        return []