def get_chunk_summary_prompt(chunk: str) -> str:
    return f"""
Summarize the following government announcement fragment.

Rules:
- Max 80 words
- Keep names, dates, places
- No assumptions

TEXT:
{chunk}
"""
