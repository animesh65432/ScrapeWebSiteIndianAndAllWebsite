from config import NORTH_INDIA
from .utils import scraping_website
async def GetJammuandKashmirAnnoucements():
    try:
        print("Scraping Jammu and Kashmir Announcements...")
        return await scraping_website(NORTH_INDIA["JammuAndKashmir"],"https://home.jk.gov.in")
    except Exception as e :
        print("Error in GetJammuandKashmirAnnoucements",e)
        return []