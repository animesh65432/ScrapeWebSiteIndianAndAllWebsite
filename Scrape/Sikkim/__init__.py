from config import config
from .utils import scrape_website

async def GetSikkimAnnouncements():
    try:
        print("Scraping Sikkim Announcements...")
        
        return await scrape_website(config["Sikkim"])
    except Exception as e:
        print("Error in GetSikkimAnnouncements", e)
        return None