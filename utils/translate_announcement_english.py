from app_types.TranslateAnnouncement import TranslateAnnouncement
from prompts.translate_announcement import (
    get_Announcement_title_prompt, 
    get_Announcement_summary_section_prompt,
    get_Announcement_details_section_prompt,
    get_Announcement_keypoints_section_prompt,
    get_Announcement_description_prompt,
    get_Announcement_category_prompt,
    get_Announcement_department_prompt
)
from typing import TypedDict
from datetime import date
from utils.format_announcement_date import format_announcement_date
from utils.call_cloudfree_api import call_cloudflare
from utils.is_big_content import is_big_content
from utils.generate_overview_big_text import generate_overview_big_text_from_title
import json
import re

class Announcement(TypedDict):
    title: str
    content: str
    source_link: str
    date: date
    state: str
    announcementId: str

def safe_parse_json(raw_text: str, field_name: str, retries: int = 0) -> dict:
    """
    Safely parse JSON with multiple fallback strategies
    """
    if not raw_text or not raw_text.strip():
        raise ValueError(f"{field_name} returned empty response")
    
    # Strategy 1: Direct parse
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        pass
    
    # Strategy 2: Extract JSON from markdown code blocks
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', raw_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    
    # Strategy 3: Find first { to last }
    start = raw_text.find('{')
    end = raw_text.rfind('}')
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(raw_text[start:end+1])
        except json.JSONDecodeError:
            pass
    
    # If all strategies fail, show what we got
    print(f"❌ Could not parse {field_name}. Raw response (first 200 chars):")
    print(f"   '{raw_text[:200]}'")
    raise ValueError(f"Failed to parse {field_name} after {retries} attempts")

async def translate_announcement_english(
    announcement: Announcement, 
    target_language: str,
    max_retries: int = 3
) -> TranslateAnnouncement:
    
    for attempt in range(1, max_retries + 1):
        try:
            if is_big_content(announcement["content"]):
                overview = await generate_overview_big_text_from_title(announcement["title"])
                announcement_copy = announcement.copy()
                announcement_copy["content"] = overview
            else:
                announcement_copy = announcement
            
            # Get prompts
            translated_title_prompt = get_Announcement_title_prompt(announcement_copy, target_language)
    
            
            summary_section_prompt = get_Announcement_summary_section_prompt(announcement_copy, target_language)
            details_section_prompt = get_Announcement_details_section_prompt(announcement_copy, target_language)
            keypoints_section_prompt = get_Announcement_keypoints_section_prompt(announcement_copy, target_language)
            
            category_prompt = get_Announcement_category_prompt(announcement_copy)
            department_prompt = get_Announcement_department_prompt(announcement_copy)
            
            # Call API for all translations
            translated_title = await call_cloudflare(translated_title_prompt)
            
            # Get sections as JSON - with validation
            summary_section_raw = await call_cloudflare(summary_section_prompt)
            details_section_raw = await call_cloudflare(details_section_prompt)
            keypoints_section_raw = await call_cloudflare(keypoints_section_prompt)
            
            category = await call_cloudflare(category_prompt)
            department = await call_cloudflare(department_prompt)
            
            
            # Validate none are empty before parsing
            if not summary_section_raw.strip():
                raise ValueError("Summary section returned empty")
            if not details_section_raw.strip():
                raise ValueError("Details section returned empty")
            if not keypoints_section_raw.strip():
                raise ValueError("Keypoints section returned empty")
            
            # Parse with safe handler
            summary_section = safe_parse_json(summary_section_raw, "summary_section", attempt)
            details_section = safe_parse_json(details_section_raw, "details_section", attempt)
            keypoints_section = safe_parse_json(keypoints_section_raw, "keypoints_section", attempt)
            
            # Validate structure with proper field checking
            if not isinstance(summary_section, dict):
                raise ValueError(f"summary is not a dict: {type(summary_section)}")
            if "content" not in summary_section:
                raise ValueError(f"summary missing 'content' field")
            
            if not isinstance(details_section, dict):
                raise ValueError(f"details is not a dict: {type(details_section)}")
            if "content" not in details_section:
                raise ValueError(f"details missing 'content' field")
            
            if not isinstance(keypoints_section, dict):
                raise ValueError(f"keypoints is not a dict: {type(keypoints_section)}")
            # KeyPoints section should have 'points' field, not 'content'
            if "points" not in keypoints_section:
                raise ValueError(f"keypoints missing 'points' field")
            if not isinstance(keypoints_section["points"], list):
                raise ValueError(f"keypoints 'points' must be a list, got {type(keypoints_section['points'])}")
            
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
            
            # Build final object
            translated = {
                "title": translated_title.strip(),
                "description": translated_description.strip(),
                "sections": sections,
                "state": announcement["state"],
                "category": category.strip(),
                "department": department.strip(),
                "date": formatted_date,
                "language": target_language,
                "source_link": announcement["source_link"],
                "announcementId": announcement["announcementId"],
            }
            
            print(f"✅ Successfully translated to {target_language}")
            
            return {
                "success": True,
                "data": translated
            }

        except (json.JSONDecodeError, ValueError) as e:
            error_msg = str(e)
            print(f"⚠️  Attempt {attempt}/{max_retries} failed: {error_msg}")
            
            if attempt < max_retries:
                print(f"   Retrying translation...")
                continue
            else:
                print(f"❌ All {max_retries} attempts failed for {target_language}")
                return {
                    "success": False,
                    "language": target_language,
                    "announcementId": announcement.get("announcementId", "unknown"),
                    "error": f"JSON parsing failed after {max_retries} attempts: {error_msg}"
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