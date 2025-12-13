from .utils import scrape_website
from config import CLOUD_FLARE_PROXY_URL
async def GetAssamAnnoucements():
    try :
        print("Scraping Assam Announcements...")
        return await scrape_website(CLOUD_FLARE_PROXY_URL["Assam"])
    except Exception as e:
        print("error in  Assam Announcements",e)
        return []