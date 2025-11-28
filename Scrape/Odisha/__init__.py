from .utils import scapre_website
from config import GovtWebiteUrl

async def GetOdishaAnnouncements():
    return scapre_website(GovtWebiteUrl["Odisha"])