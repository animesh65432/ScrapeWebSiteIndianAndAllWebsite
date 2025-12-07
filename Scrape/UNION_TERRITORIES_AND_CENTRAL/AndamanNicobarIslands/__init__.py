from config import config
from .utils import scrape_website

async def GetAndamanNicobarIslandsAnnoucements():
    try :
        print("Scraping AndamanNicobarIslands Announcements...")
        return await scrape_website(config["AndamanNicobarIslands"])
    except Exception as e :
        print("Error in GetAndamanNicobarIslandsAnnoucements",e)
        return []