def get_final_overview_prompt(summaries: str) -> str:
    return f"""
Using the summaries below, create ONE final overview.

Rules:
- Max 300 words
- Remove repetition
- Preserve facts only

SUMMARIES:
{summaries}
"""
