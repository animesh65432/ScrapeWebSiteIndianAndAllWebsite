from app_types.govt_item import GovtItem
from typing import Union

def get_prompt(item: Union[GovtItem, dict, str]) -> str:
    """
    Generate classification prompt from government item.
    Handles malformed inputs gracefully.
    """
   
    if not isinstance(item, dict):
        print(f"WARNING: get_prompt received {type(item).__name__}, returning default")
        return "news"
    
   
    title = str(item.get("title", "")).strip()
    content = str(item.get("content", "")).strip()
    link = str(item.get("link", "")).strip()
    pdf_link = str(item.get("pdf_link", "")).strip()
    
   
    if not any([title, content, link, pdf_link]):
        print("WARNING: Empty item, returning default classification")
        return "news"
    
   
    prompt = f"""You are a strict classifier. Classify the given government item into exactly ONE category:
- news
- announcement

Language may be any Indian language (Hindi, Tamil, Bengali, Marathi, Odia, etc).
Do NOT translate. Only interpret and classify based on meaning.

TITLE:
{title}

CONTENT:
{content}

PDF LINK:
{pdf_link}

PAGE LINK:
{link}

Your response must be exactly one word: "news" or "announcement"."""
    
    return prompt