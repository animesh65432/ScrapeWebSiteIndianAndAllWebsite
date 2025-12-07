from config import NORTH_INDIA
from .utils import scrape_website

async def GetChandigrahAnnoucements():
    try :
        print("Scraping Chandigarh Announcements...")
        return await scrape_website(NORTH_INDIA["Chandigarh"])
    except Exception as e :
        print("Error in GetChandigarhAnnoucements",e)
        return []