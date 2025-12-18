from typing import TypedDict

class Announcement(TypedDict):
    title: str
    content: str
    source_link: str
    date: str
    state: str
    originalAnnouncementId: str

def get_Announcement_title_prompt(original: Announcement, target_language: str) -> str:
    return f"""
You are a professional government translator.

Translate the announcement title into {target_language}.

STRICT RULES:
- Translate ONLY the given title
- Do NOT explain or interpret
- Do NOT add or remove meaning
- Keep proper nouns unchanged
- Preserve tense exactly as in the original
- If unsure, translate literally

ORIGINAL TITLE:
{original['title']}
ORIGINAL CONTENT:
{original['content']}

OUTPUT:
Only the translated title in {target_language}.
"""


def get_Announcement_description_prompt(original: Announcement, target_language: str) -> str:
    return f"""
Write a neutral factual description of this government announcement in {target_language}.

STRICT RULES:
- ONE sentence only
- Describe ONLY what is stated in the original content
- Use the same tense as the original
- Do NOT infer purpose or outcome
- Do NOT add context
- Do NOT explain significance
- If unclear, stay general

ORIGINAL:
Title: {original['title']}
Content: {original['content']}

OUTPUT:
Only the description sentence in {target_language}.
"""


def get_Announcement_state_prompt(original: Announcement, target_language: str) -> str:
    return f"""
Translate the following Indian state name into {target_language}.

STRICT RULES:
- Translate or transliterate ONLY the state name
- Do NOT add words
- Do NOT explain

STATE:
{original['state']}

OUTPUT:
Only the translated state name.
"""

def get_Announcement_content_prompt(original: Announcement, target_language: str) -> str:
    return f"""
Translate the following government announcement into {target_language}.

STRICT NON-NEGOTIABLE RULES:
- Translate sentence by sentence
- Do NOT add new information
- Do NOT remove information
- Do NOT change meaning
- Do NOT interpret intent
- Do NOT leave untranslated words (except proper nouns)
- Keep tense exactly as in the original
- Keep names, places, dates, and numbers unchanged
- If a sentence is unclear, translate literally without guessing

MARKDOWN & FORMATTING RULES:
- Use Markdown headings (##) for main titles
- Preserve all original structure and order
- Use line breaks for readability
- Use bullet points only if they exist or make sense
- Do NOT create new sections or summaries
- Bold important items (dates, times, locations)
- No decorative emojis or icons

CONTEXT:
This announcement is a **past event status report** about election duty.

ORIGINAL ANNOUNCEMENT:
Title: {original['title']}
Content:
{original['content']}

OUTPUT:
- Provide ONLY the fully translated content in {target_language}, with proper Markdown
- Start directly with the ## heading
- Do NOT include preambles, notes, or explanations
- Translate all local words into {target_language} clearly
"""