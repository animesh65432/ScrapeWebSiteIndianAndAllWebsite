from config import GovtWebiteUrl
from .utils import scraping_website
async def GetJammuandKashmirAnnoucements():
    try:
        return scraping_website(GovtWebiteUrl["JammuAndKashmir"])
    except Exception as e :
        print("Error in GetJammuandKashmirAnnoucements",e)
        return None