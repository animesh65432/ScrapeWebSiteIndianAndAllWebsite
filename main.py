import asyncio
from utils.scrape_all_states import scrape_all_states
from utils.classify_announcement_or_news import classify_announcement_or_news

async def main():
    try:
        announcements = await scrape_all_states(batch_size=3)
        classified_announcements = []
        if announcements:
            print("calling classify_announcement_or_news...")
            classified_announcements = await classify_announcement_or_news(announcements)
        
        print(classified_announcements)
        return []
            
    except Exception as e:
        print(f"❌ Critical error in main: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    asyncio.run(main())