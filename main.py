import asyncio
from utils.classify_announcement_or_news import classify_announcement_or_news
from utils.scrapthepdfcontent import extract_text_from_pdf_bytes
from utils.insert_annoucements_db import insert_annoucements_db
from service.Faiss import FaissService
# from utils.insert_translate_annoucements import insert_translate_announcements
# from service.db.Original_Annoucements import OriginalAnnouncementsDbService
from utils.load_all_regional_data import load_all_regional_data
# from utils.format_announcements import format_announcements
# from service.db.Original_Annoucements import OriginalAnnouncementsDbService
# from utils.translate_annoucements import translate_announcements


async def main():
    try:
        announcements = load_all_regional_data()

        if not announcements or len(announcements) == 0:
            print("No announcements found.")
            return []
        
        faiss_service = FaissService(announcements)
        unique_announcements = faiss_service.get_unique(threshold=0.90)
        print("unique announcements after faiss",unique_announcements)

        classified_announcements = await classify_announcement_or_news(unique_announcements)
        print("classified announcements",classified_announcements)
        announcements_with_pdf_text = await extract_text_from_pdf_bytes(classified_announcements)
        print("announcements with pdf text extracted",announcements_with_pdf_text)
        await insert_annoucements_db(announcements_with_pdf_text)

        # res = await OriginalAnnouncementsDbService().find_announcement_by_id("693c4e6c28a7e06de3b844f7")
        # fromated_res = format_announcements([res])
        # translate_res = await translate_announcements(fromated_res)

        # await insert_translate_announcements(translations=translate_res)

        print("✅ All tasks completed successfully!")

        return []

    except Exception as e:
        print(f"❌ Critical error in main: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    asyncio.run(main())
