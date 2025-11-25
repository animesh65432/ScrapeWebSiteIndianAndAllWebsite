from .utils import scrape_website
from config import config

async def GetjharkhandGovAnnoucements():
    return scrape_website(config["jharkhandGov"])