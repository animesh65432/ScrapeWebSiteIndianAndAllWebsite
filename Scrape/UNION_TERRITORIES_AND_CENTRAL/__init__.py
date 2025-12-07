from .AndamanNicobarIslands import GetAndamanNicobarIslandsAnnoucements
from .DadraandNagarHaveliDamanDiu import GetDadraandNagarHaveliDamanDiuAnnoucements
from .IndianGovtAnnoucement import GetAllIndianGovtAnnouncements
from .Ladakh import GetAllLadakhAnnoucements
from .Lakshadweep import GetLaskhadweepAnnoucements
from  utils.save_to_json import save_to_json

async def GetUNION_TERRITORIES_AND_CENTRALAnnoucements():
    try :
        print("Scraping UNION_TERRITORIES_AND_CENTRAL Announcements...")
        
        announcements = []
        announcements += await GetAllIndianGovtAnnouncements()
        announcements += await GetAndamanNicobarIslandsAnnoucements()
        announcements += await GetDadraandNagarHaveliDamanDiuAnnoucements()
        announcements += await GetAllLadakhAnnoucements()
        announcements += await GetLaskhadweepAnnoucements()

        save_to_json(announcements, "union_territories_and_central")
        
        return announcements
    except Exception as e :
        print("GetUNION_TERRITORIES_AND_CENTRALAnnoucements",e)
        return []