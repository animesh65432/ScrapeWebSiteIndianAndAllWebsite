from app_types.govt_item import GovtItem
from typing import Union

def get_prompt(item: Union[GovtItem, dict, str]) -> str:
    if not isinstance(item, dict):
        print(f"WARNING: get_prompt received {type(item).__name__}, returning default")
        return "news"
    
    title = str(item.get("title") or "").strip()
    content = str(item.get("content") or "").strip()
    
    if not title and not content:
        return "news"
    
    content_text = content if content else "(content missing, classify based on title)"
    title_text = title if title else "(title missing, classify based on content)"
    
    prompt = f"""
You are an expert classifier for INDIAN GOVERNMENT DOCUMENTS.

GOAL:
Classify the following item into ONLY ONE category:
- "announcement" → issued directly by a government authority
- "news" → media reporting, summaries, journalism, or anything not officially issued.

CLASSIFY AS "announcement" IF:
- It is issued by:
  • Central Government     • State Government
  • Ministry               • Department
  • Commission             • Authority
  • Board                  • District/Collector/DM/DC office
  • Governor/CM/PM offices
- OR contains keywords suggesting official origin in the TITLE or CONTENT:
  "Government of", "Govt. of", "Department of", "Ministry of",
  "Office of", "Collector", "District Magistrate",
  "Notification", "Order", "Public Notice", "Press Release",
  "Circular", "Tender", "Recruitment", "Vacancy",
  "RTI", "G.O.", "Scheme", "Advisory", "Amendment".

CLASSIFY AS "news" IF:
- It is journalism, reporting, media coverage, analysis, blog,
  or NOT directly issued by any government authority.

RESPONSE RULE:
Reply with ONLY ONE WORD:
"announcement" OR "news".

------------------------------
ITEM CONTENT
TITLE: {title_text}

CONTENT: {content_text}
------------------------------
"""
    return prompt
