from config import NORTHEAST_INDIA
from .utils import scrape_website

async def GetSikkimAnnouncements():
    try:
        print("Scraping Sikkim Announcements...")
        
        return await scrape_website(NORTHEAST_INDIA["Sikkim"])
    except Exception as e:
        print("Error in GetSikkimAnnouncements", e)
        return []