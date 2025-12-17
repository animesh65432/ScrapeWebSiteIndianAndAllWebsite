from app_types.TranslateAnnouncement import TranslateAnnouncement
from prompts.translate_announcement import get_Announcement_title_prompt,get_Annocement_content_prompt,get_Annocement_description_prompt,get_Annocement_state_prompt
from typing import TypedDict
from datetime import date
from service.openai import client
from utils.format_announcement_date import format_announcement_date
import asyncio

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
        
        translated_prompt = get_Announcement_title_prompt(announcement, target_language)
        translated_description_prompt = get_Annocement_description_prompt(announcement, target_language)
        translate_state_prompt = get_Annocement_state_prompt(announcement, target_language)
        translated_content_prompt = get_Annocement_content_prompt(announcement, target_language)
        translated_title_completion = await client.chat.completions.create(
                model="google/gemini-2.0-flash-exp:free",
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "You are a professional translator for government announcements. "
                            f"Translate ONLY to {target_language} script. Do not mix scripts. "
                        )
                    },
                    {"role": "user", "content": translated_prompt}
                ]
            )
        
        translated_title = translated_title_completion.choices[0].message.content.strip()

        await asyncio.sleep(4)

        translated_content_completion = await client.chat.completions.create(
                model="openai/gpt-oss-120b:free",
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "You are a professional translator for government announcements. "
                            f"Translate ONLY to {target_language} script. Do not mix scripts. "
                        )
                    },
                    {"role": "user", "content": translated_content_prompt}
                ]
            )
        
        translated_content = translated_content_completion.choices[0].message.content.strip()

        await asyncio.sleep(4)

        translated_state_completion = await client.chat.completions.create(
                model="openai/gpt-oss-120b:free",
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "You are a professional translator for government announcements. "
                            f"Translate ONLY to {target_language} script. Do not mix scripts. "
                        )
                    },
                    {"role": "user", "content": translate_state_prompt}
                ]
            )
        
        translated_state = translated_state_completion.choices[0].message.content.strip()

        await asyncio.sleep(4)
        
        translated_description_completion = await client.chat.completions.create(
                model="openai/gpt-oss-120b:free",
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "You are a professional translator for government announcements. "
                            f"Translate ONLY to {target_language} script. Do not mix scripts. "
                        )
                    },
                    {"role": "user", "content": translated_description_prompt}
                ]
            )
        
        translated_description = translated_description_completion.choices[0].message.content.strip()


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