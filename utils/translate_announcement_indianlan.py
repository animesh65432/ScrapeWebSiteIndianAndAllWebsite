from app_types.TranslateAnnouncement import TranslateAnnouncement, Section
from utils.useai4bharat import translate_using_ai4bharat

async def translate_announcement_indianLanguages(
    announcement: TranslateAnnouncement,
    target_language: str
):
    try:
        # Translate top-level fields
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

        translated_category = await translate_using_ai4bharat(
            text=announcement["category"],
            target_lang=target_language
        )

        translated_department = await translate_using_ai4bharat(
            text=announcement["department"],
            target_lang=target_language
        )

        # Translate sections
        translated_sections = []
        for section in announcement["sections"]:
            translated_section = {
                "type": section["type"],
                "heading": await translate_using_ai4bharat(
                    text=section["heading"],
                    target_lang=target_language
                )
            }
            
            # Handle different section types
            if section["type"] == "summary" or section["type"] == "details":
                translated_section["content"] = await translate_using_ai4bharat(
                    text=section["content"],
                    target_lang=target_language
                )
            elif section["type"] == "keypoints":
                translated_points = []
                for point in section["points"]:
                    translated_point = await translate_using_ai4bharat(
                        text=point,
                        target_lang=target_language
                    )
                    translated_points.append(translated_point)
                translated_section["points"] = translated_points
            
            translated_sections.append(translated_section)
        
        return {
            "success": True,
            "data": {
                **announcement,
                "title": translated_title,
                "description": translated_description,
                "sections": translated_sections,
                "language": target_language,
                "state": translated_state,
                "category": translated_category,
                "department": translated_department
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