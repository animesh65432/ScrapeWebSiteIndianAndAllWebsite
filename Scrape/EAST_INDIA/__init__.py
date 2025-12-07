from .Bihar import GetBiharAnnoucements
from .jharkhand import GetjharkhandGovAnnoucements
from .Odisha import GetOdishaAnnouncements
from .westbengal import GetwestBengalAnnoucements

async def GetEASTINDIAAnnoucements():
    try :
        BiharAnnoucements = await GetBiharAnnoucements()
        jharkhandGovAnnoucements = await GetjharkhandGovAnnoucements()
        OdishaAnnouncements = await GetOdishaAnnouncements()
        westBengalAnnoucements = await GetwestBengalAnnoucements()
        return BiharAnnoucements + jharkhandGovAnnoucements + OdishaAnnouncements + westBengalAnnoucements
    except Exception as e :
        print("GetAllEASTINDIAAnnoucements errors ",e)
        return []