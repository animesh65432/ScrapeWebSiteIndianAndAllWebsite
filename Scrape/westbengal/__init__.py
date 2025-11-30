from .utils import scrape_website
from config import config
async def GetwestBengalAnnoucements():
    try :
        return scrape_website(config["WestBengal"])
    except Exception as e:
        print("error in  scarpe_westBengal",e)
        return None