from .utils import scrape_Website
from config import GovtWebiteUrl

async def GetAllMaharashtraAnnoucements():
    try :
        print("Scraping Maharashtra Announcements...")
        return scrape_Website(GovtWebiteUrl["Maharashtra"])
    except Exception as e :
        print("GetAllMaharashtraAnnoucements",e)