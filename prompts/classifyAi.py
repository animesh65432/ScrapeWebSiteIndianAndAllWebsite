from typing import Union, Dict

def get_prompt(item: Union[Dict, dict]) -> str:
    if not isinstance(item, dict):
        return "news"
    
    title = str(item.get("title") or "").strip()
    content = str(item.get("content") or "").strip()
    department = str(item.get("department") or "").strip()
    
    if not title and not content:
        return "news"
    
    # Use more content for better classification
    if content:
        content = content[:200]
    
    # Build input
    parts = []
    if title:
        parts.append(f"Title: {title}")
    if content:
        parts.append(f"Content: {content}")
    if department:
        parts.append(f"Source: {department}")
    
    text = "\n".join(parts)
    
    return f"""{text}

Question: Is this an Announcement or News?

Announcement = Citizens can take action NOW:
- Someone can apply for a job, exam, scholarship, or scheme
- There is a registration deadline or submission date
- People can bid on tenders or contracts
- Eligible citizens can enroll or participate in something
- There are specific steps to take (apply, register, submit documents)

News = No citizen action required:
- Government officials met, spoke, or visited somewhere
- A project was inaugurated or foundation stone was laid
- Policy was discussed or a report was released
- A cultural day, festival, or observance is being marked
- Training was completed or awards were given
- General information about programs (without how to apply)

Test: Ask "Can I personally do something specific because of this information RIGHT NOW?"
- YES with deadline/steps = announcement
- NO or just general info = news

Answer ONLY with one word: announcement or news

Answer:"""
