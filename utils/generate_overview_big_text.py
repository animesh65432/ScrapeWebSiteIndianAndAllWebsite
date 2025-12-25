from utils.call_cloudfree_api import call_cloudflare
from utils.split_text import split_text
from prompts.get_chunk_summary_prompt import get_chunk_summary_prompt
from prompts.get_final_overview_prompt import get_final_overview_prompt

async def generate_overview_big_text(text: str) -> str:
    try:
        chunks = split_text(text)
        summaries = []

        for i, chunk in enumerate(chunks):
            try:
                summary = await call_cloudflare(
                    get_chunk_summary_prompt(chunk)
                )
                summaries.append(summary)
            except Exception as e:
                print(f"Error processing chunk {i}: {e}")
                continue

        if not summaries:
            raise ValueError("No chunks were successfully processed")

        combined_summaries = "\n".join(summaries)

        final_overview = await call_cloudflare(
            get_final_overview_prompt(combined_summaries)
        )

        return final_overview

    except ValueError as e:
        print(f"Validation error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error generating overview: {e}")
        raise