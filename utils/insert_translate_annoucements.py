from service.db.Translate_Annoucements import TranslateAnnouncementsDbService
from app_types.TranslateAnnouncement import TranslateAnnouncement

async def insert_translate_announcements(translations: list[TranslateAnnouncement]):
    try:
        for translation in translations:

            existing_translation = await TranslateAnnouncementsDbService.check_existing_translation(
               originalAnnouncementId=translation['originalAnnouncementId'],
               language=translation['language'] 
            )

            if not existing_translation:

                translation_id = await TranslateAnnouncementsDbService.insert_translated_announcement(translation)

                print(f"Inserted translation with id: {translation_id}")

        return "Done with inserting translations"
    except Exception as e:
        print(f"Error inserting translation: {e}")
        return None
