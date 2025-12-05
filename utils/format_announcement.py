from datetime import date, datetime
from typing import TypedDict


class Announcement(TypedDict):
    title: str
    content: str
    source_link: str
    date: date
    state: str
    originalAnnouncementId: str


def format_announcement(doc: dict) -> Announcement:
    """
    Convert MongoDB document into Announcement format with proper date handling.
    """

    raw_date = doc.get("date")
    
    print("raw_date:", raw_date)  # shows full datetime with time
    
    if isinstance(raw_date, datetime):
        formatted_date = raw_date.date()
    elif isinstance(raw_date, date):
        formatted_date = raw_date
    else:
        raise ValueError(f"Invalid date format: {raw_date}")
    
    print("formatted_date:", formatted_date)  


    return Announcement(
        title=doc.get("title", ""),
        content=doc.get("content", ""),
        source_link=doc.get("source_link", ""),
        date=formatted_date, 
        state=doc.get("state", ""),
        originalAnnouncementId=str(doc.get("_id"))  
    )
