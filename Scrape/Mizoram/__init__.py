from .utils import scrape_website
from config import config

async def GetMizoramAnnoucements():
    try :
        return scrape_website(config["Mizoram"])
    except Exception as e:
        return f"GetMizoramAnnoucements error occurred: {str(e)}"