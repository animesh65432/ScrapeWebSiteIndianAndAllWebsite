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
    
    # Extract just the date part
    if isinstance(raw_date, datetime):
        formatted_date = raw_date.date()  # This gives you just 2025-12-04
    elif isinstance(raw_date, date):
        formatted_date = raw_date
    elif isinstance(raw_date, str):
        # If it's a string like "2025-12-04T12:57:47.387Z"
        formatted_date = datetime.fromisoformat(raw_date.replace('Z', '+00:00')).date()
    else:
        raise ValueError(f"Invalid date format: {raw_date}")

    return Announcement(
        title=doc.get("title", ""),
        content=doc.get("content", ""),
        source_link=doc.get("source_link", ""),
        date=formatted_date,  
        state=doc.get("state", ""),
        announcementId=str(doc.get("_id"))
    )

def format_announcements (docs: list[Announcement]) -> list[Announcement]:
    """
    Convert a list of MongoDB documents into a list of Announcements.
    """
    return [format_announcement(doc) for doc in docs]