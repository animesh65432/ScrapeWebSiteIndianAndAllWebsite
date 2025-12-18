from app_types.TranslateAnnouncement import TranslateAnnouncement
from prompts.translate_announcement import get_Announcement_title_prompt,get_Announcement_content_prompt,get_Announcement_description_prompt,get_Announcement_state_prompt
from typing import TypedDict
from datetime import date
import httpx
from utils.format_announcement_date import format_announcement_date
from utils.call_ollama import call_ollama


class Announcement(TypedDict):
    title: str
    content: str
    source_link: str
    date: date
    state: str
    originalAnnouncementId: str



async def translate_announcement(
    announcement: Announcement, 
    target_language: str,
    max_retries: int = 3,
    debug: bool = False
) -> TranslateAnnouncement | str:
    
    try:
        
        translated_title_prompt = get_Announcement_title_prompt(announcement, target_language)
        translated_description_prompt = get_Announcement_description_prompt(announcement, target_language)
        translate_state_prompt = get_Announcement_state_prompt(announcement, target_language)
        translated_content_prompt = get_Announcement_content_prompt(announcement, target_language)

        timeout = httpx.Timeout(
            connect=10.0,
            read=None,   
            write=10.0,
            pool=10.0
        )

        async with httpx.AsyncClient(timeout=timeout) as ollama_client:
            translated_title = await call_ollama(
                prompt=translated_title_prompt,
                target_language=target_language,
                client=ollama_client
                )
    
            
            translated_content = await call_ollama(
                prompt=translated_content_prompt,
                target_language=target_language,
                client=ollama_client
            )
            
            
            translated_state = await call_ollama(
                prompt=translate_state_prompt,
                target_language=target_language,
                client=ollama_client
            )
            
            
            translated_description = await call_ollama(
                prompt=translated_description_prompt,
                target_language=target_language,
                client=ollama_client
            )


        formatted_date = format_announcement_date(announcement.get("date"))
    
        translated = {
            "title": translated_title,
            "content":translated_content,
            "description": translated_description,
            "state": translated_state,
            "originalAnnouncementId": announcement["originalAnnouncementId"],
            "date": formatted_date,
            "language": target_language,
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
            "error": str(e)
        }