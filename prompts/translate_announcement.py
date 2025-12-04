from  typing import TypedDict

class Announcement(TypedDict):
    title:str
    content:str
    source_link:str
    date:str
    state:str
    originalAnnouncementId:str

def get_translation_prompt(original: Announcement, target_language: str) -> str:
    """
    Generates an optimized prompt for AI translation of government announcements.
    
    Args:
        original: The original announcement
        target_language: Target language (e.g., 'Hindi', 'Bengali', 'Tamil', 'English')
    
    Returns:
        A detailed prompt string for AI translation
    """
    
    prompt = f"""You are an expert government announcement translator specializing in making official communications accessible to everyone, including children.

Your mission: Translate this announcement into **simple, clear {target_language}** that a 5-year-old can easily understand.

---

## **Translation Guidelines**

### **What to Translate:**
1. **Title**: Use the simplest possible words. Avoid bureaucratic language.
2. **Content**: Translate into easy, conversational {target_language}. Break complex sentences into short, simple ones.
3. **State Name**: Translate "{original['state']}" to {target_language} if applicable.

### **What to Keep:**
- ALL headings (##, ###) - translate but maintain structure
- ALL subheadings - translate but keep organization  
- ALL sections exactly as they appear
- ALL lists and bullet points - translate items but keep the list format
- ALL numbered items - translate but preserve numbering
- **Bold text** - translate but keep bold formatting
- Links - keep URLs intact, translate link text only

### **What to Remove:**
- ❌ Emojis (😊, 🎉, ✅, etc.)
- ❌ Icons and symbols (→, ★, ●, etc.)  
- ❌ Image references or descriptions
- ❌ Decorative elements that don't add meaning

### **Formatting Rules:**
- Use clean Markdown: headings (#, ##), **bold**, lists (-, 1., 2.), and links
- Keep the EXACT same structure as the original - same number of sections and lists
- If original has 5 bullet points, translation must have 5 bullet points
- If original has 3 headings, translation must have 3 headings
- Make paragraphs short (2-3 sentences max)

### **Language Style:**
- Use simple everyday words a child would know
- Avoid: legal terms, complex administrative jargon, formal government language
- Prefer: common words, active voice, direct statements
- Be culturally appropriate for {target_language} speakers in India
- Keep numbers, dates, and amounts exactly as they appear

### **Description Task:**
Write a simple 2-3 sentence summary in {target_language} that:
- Explains the main point of the announcement
- Uses very basic vocabulary
- Answers "What is this about?" in child-friendly language

---

## **Original Announcement Details**

**Title:**  
{original['title']}

**Content:**  
{original['content']}

**State:** {original['state']}  
**Date:** {original['date']}  
**Source Link:** {original['source_link']}

---

## **Required Output Format**

Respond ONLY with valid JSON. No extra text before or after.

```json
{{
  "title": "translated title in simple {target_language}",
  "content": "full translated content maintaining ALL original structure, headings, lists, and formatting in clean markdown in {target_language}",
  "description": "simple 2-3 sentence summary explaining what this announcement is about in {target_language}",
  "state": "translated state name in {target_language}"
}}
```

**IMPORTANT:** 
- Keep ALL the original structure intact
- Only translate text, never remove sections or lists
- Output must be valid JSON only
"""
    
    return prompt

