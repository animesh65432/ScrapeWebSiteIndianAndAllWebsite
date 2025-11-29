from .utils import scrape_website
from config import config

async def GetDehliAnnoucements():
    try:
        return scrape_website(config["Dehli"])
    except Exception as e:
        print("Error in Dehli_Website",e)
        return None