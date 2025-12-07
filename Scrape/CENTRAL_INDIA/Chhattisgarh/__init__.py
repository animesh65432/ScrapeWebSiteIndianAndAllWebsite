from .utils import scrape_website
from config import CENTRAL_INDIA

async def GetChhattisgarhAnnoucement():
    try :
        print("Scraping Chhattisgarh Announcements...",CENTRAL_INDIA["Chhattisgarh"])
        return await scrape_website(CENTRAL_INDIA["Chhattisgarh"])
    except Exception as e :
        print("GetChhattisgarhAnnoucement Error",e)
        return []