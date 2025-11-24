from .utils import scrape_website
from config import config

async def scrap_Dehli_Website():
    try:
        return scrape_website(config["Dehli"])
    except Exception as e:
        print("_Dehli_Website",e)