from .Andhrapradesh import GetAndhrapradeshAnnoucements
from .Karnataka import GetKarnatakaGovtAnnoucements
from .Kerala import GetKeralaGovtAnnoucements
from .TamilNadu import GetallTamilNaduAnnoucements
from .Telangana import GetAllTelanganaAnnoucements
from utils.save_to_json import save_to_json

async def GetSOUTHINDIAAnnoucements():
    try :
        print("Scraping SOUTH INDIA Announcements...")
        announcements = []
        
        announcements += await GetAndhrapradeshAnnoucements()
        announcements += await GetKarnatakaGovtAnnoucements()
        announcements += await GetKeralaGovtAnnoucements()
        announcements += await GetallTamilNaduAnnoucements()
        announcements += await GetAllTelanganaAnnoucements()

        save_to_json(announcements, "south_india")
        
        return announcements
    except Exception as e :
        print("Error in GetSOUTHINDIAAnnoucements",e)
        return []