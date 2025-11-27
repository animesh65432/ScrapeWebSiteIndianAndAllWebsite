from .utils import scrape_website
from config import config
async def GetPunjabAnnoucements():
    try :
        return scrape_website(config["Punjab"])
    except Exception as e:
        return f"GetPunjabAnnoucements error occurred: {str(e)}"