import asyncio
from utils.classify_announcement_or_news import classify_announcement_or_news
from utils.scrapthepdfcontent import extract_text_from_pdf_bytes
from utils.insert_annoucements_db import insert_annoucements_db
from service.Faiss import FaissService
# from utils.translate_annoucements import translate_announcements
# from utils.insert_translate_annoucements import insert_translate_announcements
from service.db.Original_Annoucements import OriginalAnnouncementsDbService
from utils.format_announcement import format_announcement
from utils.load_all_regional_data import load_all_regional_data

async def main():
    try:
        announcements = load_all_regional_data()

        if not announcements or len(announcements) == 0:
            print("No announcements found.")
            return []
        
        faiss_service = FaissService(announcements)
        unique_announcements = faiss_service.get_unique(threshold=0.90)
        print("unique announcements after faiss",len(unique_announcements))
        classified_announcements = await classify_announcement_or_news(unique_announcements)
        print("classified announcements",classified_announcements)
        announcements_with_pdf_text = await extract_text_from_pdf_bytes(classified_announcements)
        print("announcements with pdf text extracted",announcements_with_pdf_text)
        await insert_annoucements_db(announcements_with_pdf_text)

        print("✅ All tasks completed successfully!")

        return []

    except Exception as e:
        print(f"❌ Critical error in main: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    asyncio.run(main())
