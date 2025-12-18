from .ArunachalPradesh import GetArunachalPradeshAnnoucements
from .Assam import GetAssamAnnoucements
from .Manipur import GetAllManipurAnnoucements
from .Meghalaya import GetmeghalayaAnnoucements
from .Mizoram import GetMizoramAnnoucements
from .Nagaland import GetNagalandAnnoucements
from .Sikkim import GetSikkimAnnouncements
from .Tripura import GetAllTripuraAnnoucements
from utils.save_to_json import save_to_json
from utils.cleanup_chrome_processes import cleanup_chrome_processes
import asyncio
import os


async def GetNorthEastIndiaAnnouncements():
    """
    Scrape all North India announcements with better error handling.
    Continues even if individual scrapers fail.
    """
    results = []
    is_ci = os.getenv('GITHUB_ACTIONS') == 'true'
    
    # List of scrapers to run
    scrapers = [
        ("ArunachalPradesh", GetArunachalPradeshAnnoucements),
        ("Assam", GetAssamAnnoucements),
        ("Manipur", GetAllManipurAnnoucements),
        ("Meghalaya", GetmeghalayaAnnoucements),
        ("Mizoram", GetMizoramAnnoucements),
        ("Nagaland", GetNagalandAnnoucements),
        ("Sikkim", GetSikkimAnnouncements),
        ("Tripura", GetAllTripuraAnnoucements),
    ]
    
    failed_scrapers = []
    
    try:
        for state_name, scraper_func in scrapers:
            try:
                print(f"\n{'='*60}")
                print(f"Starting {state_name} scraper...")
                print('='*60)
                
                state_results = await scraper_func()
                
                if state_results:
                    results.extend(state_results)
                    print(f"✅ {state_name}: Added {len(state_results)} announcements")
                else:
                    print(f"⚠️  {state_name}: No announcements found")
                    failed_scrapers.append(state_name)
                
                # Cleanup between scrapers
                await cleanup_chrome_processes()
                
                # Small delay to be polite
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"❌ {state_name} scraper failed: {e}")
                failed_scrapers.append(state_name)
                
                # Try to cleanup even on error
                try:
                    await cleanup_chrome_processes()
                except:
                    pass
                
                continue  # Continue with next scraper
        
        # Final summary
        print(f"\n{'='*60}")
        print("SCRAPING SUMMARY")
        print('='*60)
        print(f"Total announcements collected: {len(results)}")
        print(f"Successful scrapers: {len(scrapers) - len(failed_scrapers)}/{len(scrapers)}")
        
        if failed_scrapers:
            print(f"Failed/Empty scrapers: {', '.join(failed_scrapers)}")
        
        # Save results
        if results:
            save_to_json(results, "northEastIndia")
        else:
            print("\n⚠️  WARNING: No announcements were collected!")
            print("   Check logs above for errors.")
            
            # Still create an empty file to indicate the script ran
            save_to_json([], "northEastIndia")
        
    except Exception as e:
        print(f"\n❌ Critical error in GetNorthIndiaAnnouncements: {e}")
        
        # Save whatever we have
        if results:
            save_to_json(results, "northEastIndia")
    
    finally:
        # Final cleanup
        await cleanup_chrome_processes()
        
        return results


if __name__ == "__main__":
    print("Starting NorthEast India Announcement Scraper...")
    print(f"Environment: {'GitHub Actions' if os.getenv('GITHUB_ACTIONS') else 'Local'}")
    asyncio.run(GetNorthEastIndiaAnnouncements())