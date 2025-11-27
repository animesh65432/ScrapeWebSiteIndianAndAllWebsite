from .utils import scrape_website
from config import config


async def GetPuducherryAnnoucements():
    try :
        return scrape_website(config["Puducherry"])
    except Exception as e:
        return f"GetPuducherryAnnoucements error occurred: {str(e)}"