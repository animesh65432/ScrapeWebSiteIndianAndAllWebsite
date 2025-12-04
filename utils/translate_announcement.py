from  app_types.TranslateAnnouncement import TranslateAnnouncement
from prompts.translate_announcement import get_translation_prompt
from service.Gemini import model
from typing import TypedDict
import json

class Announcement(TypedDict):
    title:str
    content:str
    source_link:str
    date:str
    state:str
    originalAnnouncementId:str

async def translate_announcement(annoucement: list[Announcement], target_language: str) -> TranslateAnnouncement:

    try:

        translateAnnouncement = {}

        prompt = get_translation_prompt(annoucement,target_language)

        reponse = await model.generate_content(prompt)

        raw = reponse.text

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            raw_fixed = raw[raw.find("{"): raw.rfind("}")+1]
            data = json.loads(raw_fixed)
            translateAnnouncement ={** data, }



        return data
    
    except Exception as e:
        print(f"❌ Error in translate_announcement: {e}")
        return ""