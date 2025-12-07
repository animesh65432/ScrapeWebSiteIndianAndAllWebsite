from .Bihar import GetBiharAnnoucements
from .jharkhand import GetjharkhandGovAnnoucements
from .Odisha import GetOdishaAnnouncements
from .westbengal import GetwestBengalAnnoucements
from  utils.save_to_json import save_to_json

async def GetEASTINDIAAnnoucements():
    try :
        BiharAnnoucements = await GetBiharAnnoucements()
        jharkhandGovAnnoucements = await GetjharkhandGovAnnoucements()
        OdishaAnnouncements = await GetOdishaAnnouncements()
        westBengalAnnoucements = await GetwestBengalAnnoucements()
        EASTINDIAAnnoucements = BiharAnnoucements + jharkhandGovAnnoucements + OdishaAnnouncements + westBengalAnnoucements
        save_to_json(EASTINDIAAnnoucements,"east_india")
        return EASTINDIAAnnoucements
    except Exception as e :
        print("GetAllEASTINDIAAnnoucements errors ",e)
        return []