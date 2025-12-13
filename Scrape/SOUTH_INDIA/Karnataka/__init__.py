from .utils import scrape_website
from config import CLOUD_FLARE_PROXY_URL

async def GetKarnatakaGovtAnnoucements():
    try :
        print("Scraping Karnataka Announcements...")
        return await scrape_website(CLOUD_FLARE_PROXY_URL["Karnataka"])
    except Exception as e :
        print("Error in etKarnataka_Govt_Annoucements",e)
        return []