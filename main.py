import asyncio
from utils.scrape_all_states import scrape_all_states
from utils.classify_announcement_or_news import classify_announcement_or_news
from utils.scrapthepdfcontent import extract_text_from_pdf_bytes
from utils.insert_annoucements_db import insert_annoucements_db
from service.Faiss import FaissService

async def main():
    try:
        announcements = await scrape_all_states(batch_size=3)
        print("scraped announcements from all states",len(announcements))
        faiss_service = FaissService(announcements)
        unique_announcements = faiss_service.get_unique(threshold=0.90)
        print("unique announcements after faiss",len(unique_announcements))
        classified_announcements = await classify_announcement_or_news(unique_announcements)
        print("classified announcements",classified_announcements)
        announcements_with_pdf_text = await extract_text_from_pdf_bytes(classified_announcements)
        print("announcements with pdf text extracted",announcements_with_pdf_text)
        await insert_annoucements_db(announcements_with_pdf_text)
        
        print("Inserted announcements into DB")
        print("✅ All tasks completed successfully!",len(announcements_with_pdf_text))
        # return []

    except Exception as e:
        print(f"❌ Critical error in main: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    asyncio.run(main())
