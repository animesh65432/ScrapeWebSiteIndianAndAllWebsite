from config import config
from .utils import scrape_website

async def GetChandigrahAnnoucements():
    try :
        print("Scraping Chandigarh Announcements...")
        return await scrape_website(config["Chandigarh"])
    except Exception as e :
        print("Error in GetChandigarhAnnoucements",e)
        return None