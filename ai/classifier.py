from service.Groq import Groqclient
from app_types.govt_item import GovtItem
from prompts.classifyAi import get_prompt

async def classify_ai(item: GovtItem) -> str:
    """Async classification - returns 'important' or 'skip'"""
    
    if not isinstance(item, dict):
        print(f"WARNING: classify_ai received {type(item)}, skipping")
        return "skip"
    
    # Quick pre-filter for obvious news sources
    title = str(item.get("title", "")).lower()
    source_keywords = ["times of india", "hindu", "ndtv", "news", "reporter", "correspondent"]
    if any(kw in title for kw in source_keywords):
        return "skip"
    
    prompt = get_prompt(item)
    
    try:
        response = await Groqclient.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=5,
            temperature=0
        )
        
        result = response.choices[0].message.content.strip().lower()
        
        # Normalize result
        if "important" in result:
            result = "important"
        elif "skip" in result:
            result = "skip"
        else:
            # Default to skip if unclear
            result = "skip"
        
        print(f"Classified: {result} | Title: {item.get('title', 'No title')[:60]}")
        
        return result
        
    except Exception as e:
        print(f"ERROR in classify_ai: {e}")
        return "skip"

