from .utils import scrape_website
from config import config
async def GetKeralaGovtAnnoucements():
    try :
        print("Scraping Kerala Announcements...")
        return await scrape_website(config["Kerala"])
    except Exception as e : 
        print("GetKeralaGovtAnnoucements",e)
        return []
