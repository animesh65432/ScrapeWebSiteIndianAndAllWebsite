from typing import TypedDict
from datetime import date

class TranslateAnnouncement(TypedDict):
    title:str
    content:str
    source_link:str
    date:date
    state:str
    language:str
    description:str