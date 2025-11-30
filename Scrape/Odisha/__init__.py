from .utils import scapre_website
from config import config


async def GetOdishaAnnouncements():
    try:
        print("Scraping Odisha Announcements...")
        result = scapre_website(config["Odisha"])
        return result if result else []
    except Exception as e:
        return f"GetOdishaAnnouncements error occurred: {str(e)}"