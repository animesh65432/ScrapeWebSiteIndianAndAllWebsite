from config import NORTH_INDIA
from .utils import scarpe_website

async def GetUttarPradeshAnnoucements():
    try :
        print("Scraping Uttar Pradesh Announcements...")
        return await scarpe_website(NORTH_INDIA["UttarPradesh"])
    except Exception as e :
        print("GetUttarPradeshAnnoucements",e)
        return []