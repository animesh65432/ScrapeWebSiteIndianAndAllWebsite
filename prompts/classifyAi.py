from app_types.govt_item import GovtItem
from typing import Union

def get_prompt(item: Union[GovtItem, dict, str]) -> str:
    """
    Optimized classifier for Indian government announcements.
    Focuses on actionable citizen-facing content.
    """
    if not isinstance(item, dict):
        print(f"WARNING: get_prompt received {type(item).__name__}, returning default")
        return "skip"
    
    title = str(item.get("title") or "").strip()
    content = str(item.get("content") or "").strip()
    
    if not title and not content:
        return "skip"
    
    content_text = content if content else "(content missing, classify based on title)"
    title_text = title if title else "(title missing, classify based on content)"
    
    prompt = f"""Classify this Indian government document.

OUTPUT ONLY: "important" or "skip"

Mark as "important" if it announces:
• Jobs/Recruitment/Vacancies/भर्ती
• Scholarships/Fellowships
• Welfare schemes/Yojana
• Exam dates/Results/Admit cards
• Application deadlines/Extensions
• Subsidies/Financial aid
• New policies affecting citizens
• Tenders/Contracts
• Public hearing notices
• License/Certificate procedures
• Tariff/Fee changes
• Safety alerts

Mark as "skip" if it's:
• News reporting (even about government)
• Speeches/Statements
• Meeting announcements
• Transfers/Appointments
• Event inaugurations
• Condolences/Greetings
• Progress reports

If document contains actionable information (dates, eligibility, how to apply), mark as "important".
When unsure, mark as "important" (better to include than miss).

Document can be in any Indian language.

TITLE: {title_text}
CONTENT: {content_text}

ANSWER:"""
    
    return prompt