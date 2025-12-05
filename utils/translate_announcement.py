from  app_types.TranslateAnnouncement import TranslateAnnouncement
from prompts.translate_announcement import get_translation_prompt
from service.Gemini import model
from typing import TypedDict
import json
from datetime import date
from service.openai import client

class Announcement(TypedDict):
    title:str
    content:str
    source_link:str
    date:date
    state:str
    originalAnnouncementId:str

async def translate_announcement(announcement: Announcement, target_language: str) -> TranslateAnnouncement:
    print("calling translate_announcement")
    try:
        prompt = get_translation_prompt(announcement, target_language)

        completion = await Groqclient.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that translates government announcements into simple language."},
                {"role": "user", "content": prompt}
            ],
        )

        raw = completion.choices[0].message.content.strip()

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            raw_fixed = raw[raw.find("{"): raw.rfind("}") + 1]
            data = json.loads(raw_fixed)

        translated = {
            **data,
            "originalAnnouncementId": announcement["originalAnnouncementId"],
            "date": announcement["date"],
            "language": target_language,
        }
        return translated

    except Exception as e:
        print(f"❌ Error in translate_announcement: {e}")
        return ""
