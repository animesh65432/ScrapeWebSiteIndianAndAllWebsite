from typing import TypedDict, Literal
from datetime import date

class SummarySection(TypedDict):
    type: Literal["summary"]
    heading: str
    content: str

class DetailsSection(TypedDict):
    type: Literal["details"]
    heading: str
    content: str

class KeyPointsSection(TypedDict):
    type: Literal["keypoints"]
    heading: str
    points: list[str]

Section = SummarySection | DetailsSection | KeyPointsSection

class TranslateAnnouncement(TypedDict):
    title: str
    description: str
    sections: list[Section] 
    state: str
    category: str
    department: str
    date: date
    language: str
    source_link: str
    announcementId: str
    