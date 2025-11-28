from config import config
from .utils import scrape_website

async def GetSikkimAnnouncements():
    try:
        return scrape_website(config["Sikkim"])
    except Exception as e:
        print("Error in GetSikkimAnnouncements", e)
        return None