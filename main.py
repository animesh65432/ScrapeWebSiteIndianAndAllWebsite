import asyncio
from utils.scrape_all_states import scrape_all_states
from utils.classify_announcement_or_news import classify_announcement_or_news
from utils.scrapthepdfcontent import extract_text_from_pdf_bytes

async def main():
    try:
        announcements = await scrape_all_states(batch_size=3)
        if not announcements:
            print("No announcements found.")
            return []
        
        classified_announcements = await classify_announcement_or_news(announcements)

        announcements_with_pdf_text = await extract_text_from_pdf_bytes(classified_announcements)

        print(announcements_with_pdf_text, "announcements with PDF text extracted.")
        return []

    except Exception as e:
        print(f"❌ Critical error in main: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    asyncio.run(main())
