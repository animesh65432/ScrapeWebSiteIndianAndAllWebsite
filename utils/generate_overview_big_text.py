from utils.call_cloudfree_api import call_cloudflare
from prompts.get_final_overview_prompt_from_title import get_final_overview_prompt_from_title

async def generate_overview_big_text_from_title(text: str) -> str:
    try:
        
        prompt = get_final_overview_prompt_from_title(text)

        overview = await call_cloudflare(prompt)

        return overview

    except ValueError as e:
        print(f"Validation error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error generating overview: {e}")
        raise