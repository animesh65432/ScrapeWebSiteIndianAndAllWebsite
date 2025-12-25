from app_types.TranslateAnnouncement import TranslateAnnouncement
from utils.useai4bharat import translate_using_ai4bharat

async def translate_announcement_indianLanguages(
    announcement: TranslateAnnouncement,
    target_language: str
):
    try:
        translated_title = await translate_using_ai4bharat(
            text=announcement["title"],
            target_lang=target_language
        )

        translated_description = await translate_using_ai4bharat(
            text=announcement["description"],
            target_lang=target_language
        )

        translated_state = await translate_using_ai4bharat(
            text=announcement["state"],
            target_lang=target_language
        )

        translated_content = await translate_using_ai4bharat(
            text=announcement["content"],
            target_lang=target_language
        )
        return {
            "success": True,
            "data": {
                **announcement,
                "title": translated_title,
                "description": translated_description,
                "content": translated_content,
                "language": target_language,
                "state": translated_state
            }
        }

    except Exception as e:
        print(
            f"❌ Error translating {announcement['announcementId']} → {target_language}: {e}"
        )
        return {
            "success": False,
            "error": str(e),
            "announcementId": announcement["announcementId"],
            "language": target_language
        }
