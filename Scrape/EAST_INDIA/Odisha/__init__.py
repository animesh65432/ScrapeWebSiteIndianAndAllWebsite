from .utils import scapre_website
from config import EAST_INDIA


async def GetOdishaAnnouncements():
    try:
        print("Scraping Odisha Announcements...")
        result = await scapre_website(EAST_INDIA["Odisha"])
        return result if result else []
    except Exception as e:
        print(f"GetOdishaAnnouncements error occurred: {str(e)}")
        return []