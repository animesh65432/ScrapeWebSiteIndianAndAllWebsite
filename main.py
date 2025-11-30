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


async def scrape_all_states(batch_size=3):
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
    
    print(f"\n{'='*70}")
    print(f"Starting to scrape {len(scrapers)} states/UTs in batches of {batch_size}")
    print(f"{'='*70}\n")
    
    # Process in batches
    for i in range(0, len(scraper_items), batch_size):
        batch = scraper_items[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (len(scraper_items) + batch_size - 1) // batch_size
        
        print(f"\n{'─'*70}")
        print(f"📦 Batch {batch_num}/{total_batches} - Processing {len(batch)} states")
        print(f"{'─'*70}")
        
        # Run batch scrapers concurrently
        tasks = [scraper_func() for _, scraper_func in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process batch results
        for (state_name, _), result in zip(batch, results):
            if isinstance(result, Exception):
                print(f"  ✗ {state_name}: ERROR - {str(result)[:80]}")
                total_failed += 1
                failed_states.append(state_name)
            elif result:
                if isinstance(result, list):
                    count = len(result)
                    all_announcements.extend(result)
                else:
                    count = 1
                    all_announcements.append(result)
                print(f"  ✓ {state_name}: {count} announcements")
                total_successful += 1
            else:
                print(f"  ○ {state_name}: No announcements found")
                total_successful += 1
        
        # Small delay between batches to ensure cleanup
        if i + batch_size < len(scraper_items):
            print(f"\n  ⏳ Waiting 2 seconds before next batch...")
            await asyncio.sleep(2)
    
   
    print(f"\n{'='*70}")
    print(f"📊 FINAL SUMMARY")
    print(f"{'='*70}")
    print(f"  Total States/UTs: {len(scrapers)}")
    print(f"  ✓ Successful: {total_successful}")
    print(f"  ✗ Failed: {total_failed}")
    print(f"  📄 Total Announcements Collected: {len(all_announcements)}")
    
    if failed_states:
        print(f"\n  Failed States:")
        for state in failed_states:
            print(f"    • {state}")
    
    print(f"{'='*70}\n")
    
    return all_announcements


async def main():
    try:
        
        announcements = await scrape_all_states(batch_size=3)
        
        if announcements:
            print(f"✅ Successfully collected {len(announcements)} total announcements\n")
            
            # Optional: Save to JSON file
            import json
            output_file = 'all_state_announcements.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(announcements, f, indent=2, ensure_ascii=False)
            print(f"💾 Results saved to {output_file}")
            
            return announcements
        else:
            print("⚠️  No announcements collected")
            return []
            
    except Exception as e:
        print(f"❌ Critical error in main: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    asyncio.run(main())