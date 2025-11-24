from .utils import scrape_website
from config import config
async def scarpe_westBengal_Annoucements():
    try :
        return scrape_website(config["WEST_BENGAL_ANNOUCEMENT_URL"])
    except :
        print("error in  scarpe_westBengal")
        return None