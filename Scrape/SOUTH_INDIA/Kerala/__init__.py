from .utils import scrape_website
from config import SOUTH_INDIA
async def GetKeralaGovtAnnoucements():
    try :
        print("Scraping Kerala Announcements...")
        return await scrape_website(SOUTH_INDIA["Kerala"])
    except Exception as e : 
        print("GetKeralaGovtAnnoucements",e)
        return []
