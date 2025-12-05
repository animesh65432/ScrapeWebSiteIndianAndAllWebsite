from config import config
from.utils import scarpe_website

async def GetUttarPradeshAnnoucements():
    try :
        print("Scraping Uttar Pradesh Announcements...")
        return await scarpe_website(config["UttarPradesh"])
    except Exception as e :
        print("GetUttarPradeshAnnoucements",e)
        return None