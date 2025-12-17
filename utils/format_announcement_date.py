from datetime import datetime,date
from typing import Any


def format_announcement_date(announcement_date: Any) -> datetime:
    if isinstance(announcement_date, datetime):
        return announcement_date
    elif isinstance(announcement_date, date):
        return datetime.combine(announcement_date, datetime.min.time())
    else:
        return datetime.now()

