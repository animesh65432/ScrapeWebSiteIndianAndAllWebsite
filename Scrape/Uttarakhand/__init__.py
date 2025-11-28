from .utils import scrape_website
from config import config

async def GetUttarakhandAnnouncements():
    try :
        return scrape_website(config["Uttarakhand"])
    except Exception as e :
        print("GetUttarakhandAnnouncements",e)
        return None