from config import config
from .utils import scrape_website

async def GetallTamilNaduAnnoucements():
    try :
        print("Scraping Tamil Nadu Announcements...")
        
        return await scrape_website(config["TamilNadu"])
    except Exception as e :
        print("GetallTamilNaduAnnoucements",e)
        return None