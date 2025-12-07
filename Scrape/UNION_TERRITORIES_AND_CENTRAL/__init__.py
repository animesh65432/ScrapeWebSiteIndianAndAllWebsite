from .AndamanNicobarIslands import GetAndamanNicobarIslandsAnnoucements
from .DadraandNagarHaveliDamanDiu import GetDadraandNagarHaveliDamanDiuAnnoucements
from .IndianGovtAnnoucement import GetAllIndianGovtAnnouncements
from .Ladakh import GetAllLadakhAnnoucements
from .Lakshadweep import GetLaskhadweepAnnoucements

async def GetUNION_TERRITORIES_AND_CENTRALAnnoucements():
    try :
        print("Scraping UNION_TERRITORIES_AND_CENTRAL Announcements...")
        
        announcements = []
        announcements += await GetAllIndianGovtAnnouncements()
        announcements += await GetAndamanNicobarIslandsAnnoucements()
        announcements += await GetDadraandNagarHaveliDamanDiuAnnoucements()
        announcements += await GetAllLadakhAnnoucements()
        announcements += await GetLaskhadweepAnnoucements()
        
        return announcements
    except Exception as e :
        print("GetUNION_TERRITORIES_AND_CENTRALAnnoucements",e)
        return []