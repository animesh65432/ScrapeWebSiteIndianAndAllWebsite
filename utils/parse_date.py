import datetime 

def parse_date(date_str):
    formats = [
        "%d-%b-%Y",    # 24-Nov-2025
        "%d %b, %Y",   # 24 Nov, 2025
        "%d-%b-%y",    # 24-Nov-25
        "%d %B %Y",    # 24 November 2025
        "%d %b %Y",    # 24 Nov 2025
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except:
            pass

    raise ValueError(f"❌ Unknown date format: {date_str}")
