from typing import Union, Dict

def get_prompt(item: Union[Dict, dict]) -> str:
   
    if not isinstance(item, dict):
        return "news"
    
    # Extract fields
    title = str(item.get("title") or "").strip()
    content = str(item.get("content") or "").strip()
    link = str(item.get("link") or "").strip()
    department = str(item.get("department") or "").strip()
    
    # Handle empty
    if not title and not content:
        return "news"
    
    # Truncate content aggressively (save tokens)
    if content:
        content = content[:150]  # Reduced from 200 to save tokens
    
    # Build compact info
    parts = []
    if title:
        parts.append(f"T: {title}")
    if content:
        parts.append(f"C: {content}")
    if department:
        parts.append(f"D: {department}")
    
    # URL hint
    if link:
        if ".gov.in" in link or ".nic.in" in link:
            parts.append("URL: gov.in")
        elif any(x in link for x in ["news", "ndtv", "times", "hindu"]):
            parts.append("URL: news")
    
    text = "\n".join(parts)
    
    # Compact prompt
    return f"""{text}

ACTIONABLE announcement?
YES: jobs, exams, schemes, deadlines, tenders, permits
NO: news, festivals, policy, admin, reports

announcement or news?"""