from config import config
from .utils import scrape_website

async def GetLaskhadweepAnnoucements():
    try :
        print("Scraping Lakshadweep Announcements...")
        return await scrape_website(config["Lakshadweep"])
    except Exception as e :
        print("GetLakshadweepAnnoucements",e)
        return []