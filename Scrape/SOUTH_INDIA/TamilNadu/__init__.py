from config import SOUTH_INDIA
from .utils import scrape_website

async def GetallTamilNaduAnnoucements():
    try :
        print("Scraping Tamil Nadu Announcements...")
        
        return await scrape_website(SOUTH_INDIA["TamilNadu"])
    except Exception as e :
        print("GetallTamilNaduAnnoucements",e)
        return []