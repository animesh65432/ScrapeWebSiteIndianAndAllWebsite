from config import config
from .utils import scrape_website

async def GetAllIndianGovtAnnouncements():
    try:
        res = await scrape_website(config["IndianGovtAnnouncement"])
        return res
    except Exception as e:
        print("GetAllIndianGovtAnnouncements", e)
        return []