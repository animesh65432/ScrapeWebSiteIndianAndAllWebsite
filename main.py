import asyncio
import traceback
from utils.classify_announcement_or_news import classify_announcement_or_news
from utils.scrapthepdfcontent import extract_text_from_pdf_bytes
from utils.insert_annoucements_db import insert_annoucements_db
from service.Faiss import FaissService
from utils.insert_translate_annoucements import insert_translate_announcements
from utils.load_all_regional_data import load_all_regional_data
from service.db.Original_Annoucements import OriginalAnnouncementsDbService
from utils.format_announcements import format_announcements
from utils.translate_annoucements import translate_announcements

async def main():
    try:
        # announcements = load_all_regional_data()
        # if not announcements or len(announcements) == 0:
        #     print("No announcements found.")
        #     return []
        
        # faiss_service = FaissService(announcements)
        # unique_announcements = faiss_service.get_unique(threshold=0.90)
        # classified_announcements = await classify_announcement_or_news(unique_announcements)
        # announcements_with_pdf_text = await extract_text_from_pdf_bytes(classified_announcements)
        # new_annoucments = await insert_annoucements_db(announcements_with_pdf_text)
        new_annoucments = await OriginalAnnouncementsDbService.find_announcements()  # For now, skip previous steps
        fromated_res = format_announcements(new_annoucments[:1])
        translate_res = await translate_announcements(fromated_res)
        await insert_translate_announcements(translations=translate_res)
        
        print("✅ All tasks completed successfully!",translate_res)
        return []

    except Exception as e:
        print(f"❌ Critical error in main: {e}")
        traceback.print_exc()
        return None


if __name__ == "__main__":
    asyncio.run(main())
