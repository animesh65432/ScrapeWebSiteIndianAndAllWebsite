from utils.call_cloudfree_api import call_cloudflare
from utils.split_text import split_text
from prompts.get_chunk_summary_prompt import get_chunk_summary_prompt
from prompts.get_final_overview_prompt import get_final_overview_prompt

def generate_overview_big_text(text: str) -> str:
    chunks = split_text(text)
    summaries = []

    for chunk in chunks:
        summary = call_cloudflare(
            get_chunk_summary_prompt(chunk),
            max_tokens=128
        )
        summaries.append(summary)

    combined_summaries = "\n".join(summaries)

    final_overview = call_cloudflare(
        get_final_overview_prompt(combined_summaries),
        max_tokens=512
    )

    return final_overview
