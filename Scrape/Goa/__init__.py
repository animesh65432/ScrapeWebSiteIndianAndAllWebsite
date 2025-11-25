from .utils import scrape_website
from config import config

async def scrape_Goa_Annoucements():
    try:
        return scrape_website(config["Goa"])
    except Exception as e :
        print("scrape_Goa_Annoucements",e)
