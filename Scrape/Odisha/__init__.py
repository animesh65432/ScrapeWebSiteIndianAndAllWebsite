from .utils import scapre_website
from config import GovtWebiteUrl

async def GetOdishaAnnouncements():
    try:
        return scapre_website(GovtWebiteUrl["Odisha"])
    except Exception as e:
        return f"GetOdishaAnnouncements error occurred: {str(e)}"