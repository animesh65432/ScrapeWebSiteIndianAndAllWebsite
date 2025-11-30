from .utils import scrape_website
from config import config
async def GetAssamAnnoucements():
    try :
        return scrape_website(config["Assam"])
    except Exception as e:
        print("error in  scarpe_westBengal",e)
        return None