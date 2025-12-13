from .utils import scrape_website
from config import CLOUD_FLARE_PROXY_URL

async def GetChhattisgarhAnnoucement():
    try :
        print("Scraping Chhattisgarh Announcements...",CLOUD_FLARE_PROXY_URL["Chhattisgarh"])
        return await scrape_website(CLOUD_FLARE_PROXY_URL["Chhattisgarh"])
    except Exception as e :
        print("GetChhattisgarhAnnoucement Error",e)
        return []