def is_big_content(text: str) -> bool:
    if not text:
        return False
    return len(text) > 3500
