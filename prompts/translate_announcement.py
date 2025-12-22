from typing import TypedDict

class Announcement(TypedDict):
    title: str
    content: str
    source_link: str
    date: str
    state: str
    originalAnnouncementId: str

def get_Announcement_content_prompt(original: Announcement, target_language: str) -> str:
    return f"""Translate the following announcement to {target_language}.

SOURCE:
{original['content']}

INSTRUCTIONS:

1. Follow this exact structure:

## [Brief title in {target_language}]
**Ref:** [reference number] | **Date:** [date] | **Loc:** [location, state]

### Summary
- Write ~30 words summarizing the announcement.
- Include who, what, when, and where.
- Avoid repeating any sentence from Details or Key Information.

### Details
- Write ~30 words adding more context, background, or extra details.
- Include timing, locations, outcomes, or relevant activities.
- Avoid repeating any sentence from Summary or Key Information.

**Key Information:**
- Write 4 bullets, each presenting **unique information** not in Summary or Details.
- Use '-' for bullets (do NOT use '*' or other symbols).
- Focus on important points such as personnel, activities, or milestones.

STRICT RULES:
- NEVER translate or expand acronyms: LADC, MDC
- NEVER translate place names (e.g., Lawngtlai, Government Lawngtlai College)
- Keep all proper nouns unchanged
- Remove filler words like: te chuan, khan, a ni, hian
- Avoid repeating any sentence or phrase across sections

COMPLETION:
- Keep total under 200 words
- Finish the entire structure before stopping
- Output must be 100% {target_language}
- Do NOT include placeholders like [X] or instructions

Begin translation:"""



def get_Announcement_title_prompt(original: Announcement, target_language: str) -> str:
    return f"""
Translate this title into clear, natural {target_language}.

RULES:
- Keep acronyms (LADC, MDC)
- Keep place names
- Make the action/event CLEAR (e.g., "Arrival", "Update", "Announcement")
- Avoid vague phrases like "Order to District"
- Maximum 80 characters
- Focus on WHAT HAPPENED, not administrative details

ORIGINAL: {original['title']}
{'' if original.get('title') else f"CONTENT: {original.get('content', '')}"}

EXAMPLES OF GOOD TITLES:
- "LADC-MDC Election 2025 - Officials Arrive in Lawngtlai"
- "LADC-MDC Election 2025 - Safe Arrival Update"
- "Election Officials Return to Lawngtlai - LADC-MDC 2025"

OUTPUT: Only the improved title.
"""

def get_Announcement_description_prompt(content: str, target_language: str) -> str:
    return f"""
Write a one-sentence description of this announcement in {target_language}.

CONTENT:
{content}

RULES:
- ONE sentence only
- Use only {target_language} script
- Summarize the main event/action
- Include key details (date, location, purpose)

OUTPUT: Only the description sentence.
"""

def get_Announcement_state_prompt(original: Announcement, target_language: str) -> str:
    return f"""
Translate this Indian state name to {target_language}: {original['state']}

Requirements:
- Use the official {target_language} name for this Indian state
- If the state name is not from India, return "IndianGovt" translated to {target_language}
- Return ONLY the translated state name, nothing else

Example for Hindi:
Input: "Maharashtra"
Output: "महाराष्ट्र"
"""