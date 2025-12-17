from typing import TypedDict

class Announcement(TypedDict):
    title: str
    content: str
    source_link: str
    date: str
    state: str
    originalAnnouncementId: str

def get_Announcement_title_prompt(original: Announcement, target_language: str) -> str:
    prompt = f"""You are an expert government announcement translator specializing in making official communications accessible to everyone.

Translate this announcement title into simple, clear {target_language}.

---

## TRANSLATION GUIDELINES

### Language Style:
- Use simple everyday words that common people understand
- Avoid legal/administrative jargon - use plain language equivalents
- Be culturally appropriate for {target_language} speakers in India
- Make it sound natural, as if a local person is explaining it to their neighbor

---

## ORIGINAL ANNOUNCEMENT

**Title:** {original['title']}

---

## OUTPUT REQUIREMENTS

**CRITICAL: Output ONLY the translated title. No extra text, no explanations, no formatting.**

Respond with just the translated title in {target_language}."""
    
    return prompt

def get_Annocement_description_prompt(original: Announcement, target_language: str) -> str:
    prompt = f"""You are an expert government announcement translator specializing in making official communications accessible to everyone.

Write a brief description of this announcement in simple, clear {target_language}.

---

## DESCRIPTION GUIDELINES

### Language Style:
- Write in {target_language} ONLY (do not mix languages)
- Keep it 2-3 sentences maximum
- Explain the main point: What is this announcement about? Who does it affect? What action (if any) should people take?
- Use simple, everyday language that anyone can understand
- Be culturally appropriate for {target_language} speakers in India
- Make it sound natural, as if a local person is explaining it to their neighbor

---

## ORIGINAL ANNOUNCEMENT

**Title:** {original['title']}
**Content:** {original['content']}

---

## OUTPUT REQUIREMENTS

**CRITICAL: Output ONLY the description text. No extra text, no explanations, no formatting.**

Respond with just the 2-3 sentence description in {target_language}."""

    return prompt


def get_Annocement_state_prompt(original: Announcement, target_language: str) -> str:
    prompt = f"""You are an expert translator.

Translate this Indian state name into {target_language}.

---

## TRANSLATION GUIDELINES

- Use the official name commonly used in {target_language}
- Keep it simple and recognizable
- Use standard transliteration if needed

---

## ORIGINAL STATE

**State:** {original['state']}

---

## OUTPUT REQUIREMENTS

**CRITICAL: Output ONLY the translated state name. No extra text, no explanations, no formatting.**

Respond with just the state name in {target_language}."""

    return prompt


def get_Annocement_content_prompt(original: Announcement, target_language: str) -> str:
    prompt = f"""You are an expert government announcement translator specializing in making official communications accessible to everyone.

Translate this announcement content into simple, clear {target_language}.

---

## TRANSLATION GUIDELINES

### Content Structure:
- If the original content has headings, subheadings, lists - keep them
- If the original content lacks structure, organize it into clear sections with markdown headings (##, ###)
- Break long paragraphs into shorter, readable sections
- Use bullet points (-) or numbered lists (1., 2., 3.) for steps, benefits, or multiple items
- Add appropriate headings like "## मुख्य बातें" (Key Points), "## पात्रता" (Eligibility), "## कैसे आवेदन करें" (How to Apply), etc. based on content

### What to Keep:
- ALL existing headings, subheadings, lists, and structure
- Markdown formatting (##, **, -, etc.)
- Numbers, dates, and amounts exactly as they appear
- Links (translate link text, keep URLs)

### What to Remove:
- Emojis and decorative icons
- Image references
- Decorative elements without meaning

### Language Style:
- Use simple everyday words that common people understand
- Avoid legal/administrative jargon - use plain language equivalents
- Use active voice and direct statements
- Be culturally appropriate for {target_language} speakers in India
- Make it sound natural, as if a local person is explaining it to their neighbor
- Write EVERYTHING in {target_language} script only - do not mix English words or other scripts

### Formatting Enhancement:
- Use **bold** for important terms, amounts, or dates
- Use line breaks (blank lines) between sections for readability
- If there are steps or procedures, present them as numbered lists
- If there are benefits or features, present them as bullet points

---

## ORIGINAL ANNOUNCEMENT

**Content:** {original['content']}

---

## OUTPUT REQUIREMENTS

**CRITICAL: Output ONLY the translated content with proper markdown structure. No extra text, no explanations, no preamble.**

Respond with just the well-structured, translated content in {target_language} with clear markdown formatting."""

    return prompt