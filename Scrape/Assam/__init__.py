from .utils import scrape_website
from config import config
async def scarpe_Assam_Annoucements():
    try :
        return scrape_website(config["Assam"])
    except Exception as e:
        print("error in  scarpe_westBengal",e)
        return None