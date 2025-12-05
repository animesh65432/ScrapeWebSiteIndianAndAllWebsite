from .utils import scrape_website
from config import config

async def GetRajasthanAnnoucements():
    try:
        print("Scraping Rajasthan Announcements...")
        return await scrape_website(config["Rajasthan"])
    except Exception as e:
        print(f"Error in GetRajasthanAnnoucements: {e}")
        return ""