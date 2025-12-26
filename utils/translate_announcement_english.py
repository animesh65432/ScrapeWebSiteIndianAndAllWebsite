from app_types.TranslateAnnouncement import TranslateAnnouncement
from prompts.translate_announcement import (
    get_Announcement_title_prompt, 
    get_Announcement_summary_section_prompt,
    get_Announcement_details_section_prompt,
    get_Announcement_keypoints_section_prompt,
    get_Announcement_description_prompt, 
    get_Announcement_state_prompt,
    get_Announcement_category_prompt,
    get_Announcement_department_prompt
)
from typing import TypedDict
from datetime import date
from utils.format_announcement_date import format_announcement_date
from utils.call_cloudfree_api import call_cloudflare
from utils.is_big_content import is_big_content
from utils.generate_overview_big_text import generate_overview_big_text
import json

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
) -> dict:
    
    try:
        if is_big_content(announcement["content"]):
            overview = await generate_overview_big_text(announcement["content"])
            announcement_copy = announcement.copy()
            announcement_copy["content"] = overview
        else:
            announcement_copy = announcement
        
        translated_title_prompt = get_Announcement_title_prompt(announcement_copy, target_language)
        translate_state_prompt = get_Announcement_state_prompt(announcement_copy, target_language)
        
        # Section prompts
        summary_section_prompt = get_Announcement_summary_section_prompt(announcement_copy, target_language)
        details_section_prompt = get_Announcement_details_section_prompt(announcement_copy, target_language)
        keypoints_section_prompt = get_Announcement_keypoints_section_prompt(announcement_copy, target_language)
        
        # Category and department (no target_language needed)
        category_prompt = get_Announcement_category_prompt(announcement_copy)
        department_prompt = get_Announcement_department_prompt(announcement_copy)
        
        # Call API for all translations
        translated_title = await call_cloudflare(translated_title_prompt)
        translated_state = await call_cloudflare(translate_state_prompt)
        
        # Get sections as JSON
        summary_section_raw = await call_cloudflare(summary_section_prompt)
        details_section_raw = await call_cloudflare(details_section_prompt)
        keypoints_section_raw = await call_cloudflare(keypoints_section_prompt)
        
        category = await call_cloudflare(category_prompt)
        department = await call_cloudflare(department_prompt)
        
        # Parse JSON sections
        try:
            summary_section = json.loads(summary_section_raw)
            details_section = json.loads(details_section_raw)
            keypoints_section = json.loads(keypoints_section_raw)
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            raise ValueError(f"Failed to parse section JSON: {e}")
        
        # Build sections array
        sections = [summary_section, details_section, keypoints_section]
        
        # Generate description from summary content
        description_prompt = get_Announcement_description_prompt(
            summary_section["content"], 
            target_language
        )

        translated_description = await call_cloudflare(description_prompt)
        
        # Format date
        formatted_date = format_announcement_date(announcement.get("date"))
        
        # Build final object matching TranslateAnnouncement type
        translated = {
            "title": translated_title.strip(),
            "description": translated_description.strip(),
            "sections": sections,
            "state": translated_state.strip(),
            "category": category.strip(),
            "department": department.strip(),
            "date": formatted_date,
            "language": target_language,
            "source_link": announcement["source_link"],
            "announcementId": announcement["announcementId"],
        }
        
        print(f"✅ Successfully translated to {translated}")
        
        return {
            "success": True,
            "data": translated
        }

    except Exception as e:
        error_msg = str(e)
        print(f"❌ Translation failed for {target_language}: {error_msg}")
        
        return {
            "success": False,
            "language": target_language,
            "announcementId": announcement.get("announcementId", "unknown"),
            "error": error_msg
        }