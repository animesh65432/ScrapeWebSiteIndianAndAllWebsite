import asyncio
from Scrape.westbengal import GetwestBengalAnnoucements
from Scrape.Assam import GetAssamAnnoucements
from Scrape.Dehli import GetDehliAnnoucements
from Scrape.Goa import GetGoaAnnoucements
from Scrape.HimachalPradesh import GetHimachalPradeshAnnoucements
from Scrape.ArunachalPradesh import GetArunachalPradeshAnnoucements
from Scrape.Chandigarh import GetChandigrahAnnoucements
from Scrape.JammuandKashmir import GetJammuandKashmirAnnoucements
from Scrape.jharkhand import GetjharkhandGovAnnoucements
from Scrape.Karnataka import GetKarnatakaGovtAnnoucements
from Scrape.Kerala import GetKeralaGovtAnnoucements
from Scrape.Ladakh import GetAllLadakhAnnoucements
from Scrape.Maharashtra import GetAllMaharashtraAnnoucements
from Scrape.MadhyaPradesh import GetAllMadhyaPradeshAnnoucements
from Scrape.Manipur import GetAllManipurAnnoucements
from Scrape.Meghalaya import GetmeghalayaAnnoucements
from Scrape.Mizoram import GetMizoramAnnoucements
from Scrape.Nagaland import GetNagalandAnnoucements
from Scrape.Odisha import GetOdishaAnnouncements
from Scrape.Puducherry import GetPuducherryAnnoucements
from Scrape.Punjab import GetPunjabAnnoucements
from Scrape.Rajasthan import GetRajasthanAnnoucements
from Scrape.Sikkim import GetSikkimAnnouncements
from Scrape.TamilNadu import GetallTamilNaduAnnoucements
from Scrape.Telangana import GetAllTelanganaAnnoucements
from Scrape.Tripura import GetAllTripuraAnnoucements
from Scrape.Uttarakhand import GetUttarakhandAnnouncements
from Scrape.UttarPradesh import GetUttarPradeshAnnoucements
from Scrape.Gujarat import GetGujaratAnnoucements
from Scrape.Haryana import GetHaryanaAnnoucements
from Scrape.Lakshadweep import GetLaskhadweepAnnoucements
from Scrape.DadraandNagarHaveliDamanDiu import GetDadraandNagarHaveliDamanDiuAnnoucements
from Scrape.AndamanNicobarIslands import GetAndamanNicobarIslandsAnnoucements
from Scrape.Bihar import GetBiharAnnoucements
from Scrape.Andhrapradesh import GetAndhrapradeshAnnoucements
from Scrape.IndianGovtAnnoucement import GetAllIndianGovtAnnouncements
from utils.cleanup_chrome_processes import cleanup_chrome_processes

async def scrape_all_states(batch_size=1, max_concurrent=1):
    scrapers = {
        "West Bengal": GetwestBengalAnnoucements,
        "Assam": GetAssamAnnoucements,
        "Delhi": GetDehliAnnoucements,
        "Goa": GetGoaAnnoucements,
        "Himachal Pradesh": GetHimachalPradeshAnnoucements,
        "Arunachal Pradesh": GetArunachalPradeshAnnoucements,
        "Chandigarh": GetChandigrahAnnoucements,
        "Jammu and Kashmir": GetJammuandKashmirAnnoucements,
        "Jharkhand": GetjharkhandGovAnnoucements,
        "Karnataka": GetKarnatakaGovtAnnoucements,
        "Kerala": GetKeralaGovtAnnoucements,
        "Ladakh": GetAllLadakhAnnoucements,
        "Maharashtra": GetAllMaharashtraAnnoucements,
        "Madhya Pradesh": GetAllMadhyaPradeshAnnoucements,
        "Manipur": GetAllManipurAnnoucements,
        "Meghalaya": GetmeghalayaAnnoucements,
        "Mizoram": GetMizoramAnnoucements,
        "Nagaland": GetNagalandAnnoucements,
        "Odisha": GetOdishaAnnouncements,
        "Puducherry": GetPuducherryAnnoucements,
        "Punjab": GetPunjabAnnoucements,
        "Rajasthan": GetRajasthanAnnoucements,
        "Sikkim": GetSikkimAnnouncements,
        "Tamil Nadu": GetallTamilNaduAnnoucements,
        "Telangana": GetAllTelanganaAnnoucements,
        "Tripura": GetAllTripuraAnnoucements,
        "Uttarakhand": GetUttarakhandAnnouncements,
        "Uttar Pradesh": GetUttarPradeshAnnoucements,
        "Gujarat": GetGujaratAnnoucements,
        "Haryana": GetHaryanaAnnoucements,
        "Lakshadweep": GetLaskhadweepAnnoucements,
        "Dadra and Nagar Haveli & Daman and Diu": GetDadraandNagarHaveliDamanDiuAnnoucements,
        "Andaman and Nicobar Islands": GetAndamanNicobarIslandsAnnoucements,
        "Bihar": GetBiharAnnoucements,
        "Andhra Pradesh": GetAndhrapradeshAnnoucements,
        "Indian Govt Announcement": GetAllIndianGovtAnnouncements
    }
    
    scraper_items = list(scrapers.items())
    all_announcements = []
    total_successful = 0
    total_failed = 0
    failed_states = []
    
    semaphore = asyncio.Semaphore(max_concurrent)
    
    print(f"\n{'='*70}")
    print(f"Starting to scrape {len(scrapers)} states/UTs")
    print(f"Batch: {batch_size} | Max Concurrent: {max_concurrent}")
    print(f"{'='*70}\n")
    
    async def run_with_limit(state_name, scraper_func):
        async with semaphore:
            try:
                result = await scraper_func()
                return state_name, result, None
            except Exception as e:
                print(f"[run_with_limit] Exception in {state_name}: {e}")
                return state_name, None, e
    
    for i in range(0, len(scraper_items), batch_size):
        batch = scraper_items[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (len(scraper_items) + batch_size - 1) // batch_size
        
        print(f"\n{'─'*70}")
        print(f"📦 Batch {batch_num}/{total_batches} - {len(batch)} states")
        print(f"{'─'*70}")
        
        tasks = [run_with_limit(name, func) for name, func in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            # Handle exceptions from gather
            if isinstance(result, Exception):
                print(f"  ✗ Batch error: {result}")
                total_failed += 1
                continue
            
            state_name, data, error = result
            
            if error:
                print(f"  ✗ {state_name}: {str(error)[:60]}")
                total_failed += 1
                failed_states.append(state_name)
            elif data:
                if isinstance(data, list):
                    count = len(data)
                    if count > 0:
                        all_announcements.extend(data)
                        print(f"  ✓ {state_name}: {count} announcements")
                        total_successful += 1
                    else:
                        print(f"  ○ {state_name}: No announcements")
                        total_successful += 1
                elif isinstance(data, dict):
                    all_announcements.append(data)
                    print(f"  ✓ {state_name}: 1 announcement")
                    total_successful += 1
            else:
                print(f"  ○ {state_name}: No announcements")
                total_successful += 1
        
        # Cleanup between batches
        if i + batch_size < len(scraper_items):
            print(f"\n  ⏳ Waiting and cleaning up...")
            await asyncio.sleep(3)
            
            if batch_num % 1 == 0:
                print(f"  🧹 Deep cleanup (batch {batch_num})...")
                await cleanup_chrome_processes()
                await asyncio.sleep(2)
    
    print(f"\n{'='*70}")
    print(f"📊 SUMMARY")
    print(f"{'='*70}")
    print(f"  States: {len(scrapers)}")
    print(f"  ✓ Success: {total_successful}")
    print(f"  ✗ Failed: {total_failed}")
    print(f"  📄 Total: {len(all_announcements)}")
    
    if failed_states:
        print(f"\n  Failed: {', '.join(failed_states)}")
    
    print(f"{'='*70}\n")
    return all_announcements