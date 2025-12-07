from .Chandigarh import GetChandigrahAnnoucements
from .Dehli import GetDehliAnnoucements
from .Haryana import GetHaryanaAnnoucements
from .HimachalPradesh import GetHimachalPradeshAnnoucements
from .JammuandKashmir import GetJammuandKashmirAnnoucements
from .Punjab import GetPunjabAnnoucements
from .Uttarakhand import GetUttarakhandAnnouncements
from .UttarPradesh import GetUttarPradeshAnnoucements
from utils.save_to_json import save_to_json
from utils.cleanup_chrome_processes import cleanup_chrome_processes
import asyncio

async def GetNorthIndiaAnnouncements():
    results = []
    try:
        results.extend(await GetChandigrahAnnoucements())
        await cleanup_chrome_processes()
        results.extend(await GetDehliAnnoucements())
        await cleanup_chrome_processes()
        results.extend(await GetHaryanaAnnoucements())
        await cleanup_chrome_processes()
        results.extend(await GetHimachalPradeshAnnoucements())
        await cleanup_chrome_processes()
        results.extend(await GetJammuandKashmirAnnoucements())
        await cleanup_chrome_processes()
        results.extend(await GetPunjabAnnoucements())
        await cleanup_chrome_processes()
        results.extend(await GetUttarakhandAnnouncements())
        await cleanup_chrome_processes()
        results.extend(await GetUttarPradeshAnnoucements())

        save_to_json(results, "northIndia")
        
    except Exception as e:
        print("Error in GetNorthIndiaAnnouncements:", e)
    finally:
        return results
    
if __name__ == "__main__":
    asyncio.run(GetNorthIndiaAnnouncements())