from config import config
from .utils import scraping_website
async def GetJammuandKashmirAnnoucements():
    try:
        return scraping_website(config["JammuAndKashmir"],"https://home.jk.gov.in")
    except Exception as e :
        print("Error in GetJammuandKashmirAnnoucements",e)
        return None