def split_text(text: str, max_chars: int = 1200):
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
