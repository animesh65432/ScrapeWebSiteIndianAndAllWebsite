from .Chandigarh import GetChandigrahAnnoucements
from .Dehli import GetDehliAnnoucements
from .Haryana import GetHaryanaAnnoucements
from .HimachalPradesh import GetHimachalPradeshAnnoucements
from .JammuandKashmir import GetJammuandKashmirAnnoucements
from .Punjab import GetPunjabAnnoucements
from .Uttarakhand import GetUttarakhandAnnouncements
from .UttarPradesh import GetUttarPradeshAnnoucements


async def GetNorthIndiaAnnouncements():
    results = []
    try:
        results.extend(await GetChandigrahAnnoucements())
        results.extend(await GetDehliAnnoucements())
        results.extend(await GetHaryanaAnnoucements())
        results.extend(await GetHimachalPradeshAnnoucements())
        results.extend(await GetJammuandKashmirAnnoucements())
        results.extend(await GetPunjabAnnoucements())
        results.extend(await GetUttarakhandAnnouncements())
        results.extend(await GetUttarPradeshAnnoucements())
    except Exception as e:
        print("Error in GetNorthIndiaAnnouncements:", e)
    finally:
        return results