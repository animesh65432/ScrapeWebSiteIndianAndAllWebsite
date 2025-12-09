from .utils import scrape_website
from config import SOUTH_INDIA

async def GetKarnatakaGovtAnnoucements():
    try :
        print("Scraping Karnataka Announcements...")
        return await scrape_website(SOUTH_INDIA["Karnataka"])
    except Exception as e :
        print("Error in etKarnataka_Govt_Annoucements",e)
        return []