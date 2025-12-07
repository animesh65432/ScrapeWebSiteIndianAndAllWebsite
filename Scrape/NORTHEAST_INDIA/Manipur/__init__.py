from .utils import scrape_website
from config import config

async def GetAllManipurAnnoucements():
    try :
        print("Scraping Manipur Announcements...")
        
        return await scrape_website(config["Manipur"])
    except Exception as e :
        print("GetAllManipurAnnoucements",e)

        return []