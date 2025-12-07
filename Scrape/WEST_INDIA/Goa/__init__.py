from .utils import scrape_website
from config import config

async def GetGoaAnnoucements():
    try:
        print("Scraping Goa Announcements...")
        return await scrape_website(config["Goa"])
    except Exception as e :
        print("Error in scrape_Goa_Annoucements",e)
        return []
