from typing import TypedDict
from datetime import date

class OriginalAnnouncement(TypedDict):
    title:str
    content:str
    source_link:str
    date:date
    state:str