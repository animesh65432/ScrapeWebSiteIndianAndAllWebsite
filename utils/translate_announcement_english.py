from app_types.TranslateAnnouncement import TranslateAnnouncement
from prompts.translate_announcement import get_Announcement_title_prompt, get_Announcement_content_prompt, get_Announcement_description_prompt, get_Announcement_state_prompt
from typing import TypedDict
from datetime import date
from utils.format_announcement_date import format_announcement_date
from utils.call_cloudfree_api import call_cloudflare
from utils.is_big_content import is_big_content
from utils.generate_overview_big_text import generate_overview_big_text

class Announcement(TypedDict):
    title: str
    content: str
    source_link: str
    date: date
    state: str
    announcementId: str

async def translate_announcement_english(
    announcement: Announcement, 
    target_language: str,
) -> list[TranslateAnnouncement]:
    
    try:
        translated_title_prompt = get_Announcement_title_prompt(announcement, target_language)
        translate_state_prompt = get_Announcement_state_prompt(announcement, target_language)

        if is_big_content(announcement["content"]):
            overview = await generate_overview_big_text(announcement["content"])
            announcement["content"] = overview
            translated_content_prompt = get_Announcement_content_prompt(announcement, target_language)
        else:
            translated_content_prompt = get_Announcement_content_prompt(announcement, target_language)

        translated_title = await call_cloudflare(translated_title_prompt)
        translated_content = await call_cloudflare(translated_content_prompt)
        translated_state = await call_cloudflare(translate_state_prompt)
        
        translated_description_prompt = get_Announcement_description_prompt(translated_content, target_language)
        translated_description = await call_cloudflare(translated_description_prompt)
        
        formatted_date = format_announcement_date(announcement.get("date"))
    
        translated = {
            "title": translated_title,
            "content": translated_content,
            "description": translated_description,
            "state": translated_state,
            "announcementId": announcement["announcementId"],
            "date": formatted_date,
            "language": "en",
            "source_link": announcement["source_link"],
        }
            
        print(f"✅ Successfully translated to {target_language}")
        
        return {
            "success": True,
            "data": translated
        }

    except Exception as e:
        error_msg = str(e)
        print(f"❌ failed for {target_language}: {error_msg} id:{announcement['originalAnnouncementId']}")
        
        return {
            "success": False,
            "language": target_language,
            "originalAnnouncementId": announcement["originalAnnouncementId"],
            "error": error_msg
        }