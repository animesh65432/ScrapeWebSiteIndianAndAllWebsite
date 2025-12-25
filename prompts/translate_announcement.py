from typing import TypedDict

class Announcement(TypedDict):
    title: str
    content: str
    source_link: str
    date: str
    state: str
    originalAnnouncementId: str

def get_Announcement_content_prompt(original: Announcement, target_language: str) -> str:
    # Detect what metadata exists in source
    has_ref = '**Ref:**' in original['content']
    has_date = '**Date:**' in original['content']
    has_loc = '**Loc:**' in original['content']
    
    # Build metadata template
    metadata_parts = []
    if has_ref:
        metadata_parts.append("**Ref:** [exact value from source]")
    if has_date:
        metadata_parts.append("**Date:** [translate month only, keep numbers]")
    if has_loc:
        metadata_parts.append("**Loc:** [translate location]")
    
    metadata_line = " | ".join(metadata_parts)
    
    return f"""You are translating a government announcement to {target_language}.

SOURCE:
{original['content']}

YOUR TASK: Translate to {target_language} following this EXACT structure:

## [Title in {target_language}]
{metadata_line if metadata_parts else "[No metadata line - go directly to Summary]"}

### Summary
[2-3 complete sentences about WHO did WHAT, WHEN, WHERE, and WHY]

### Details
[2-3 complete sentences with additional context, attendees, or significance]

**Key Information:**
- [First important point - complete sentence]
- [Second important point - complete sentence]
- [Third important point - complete sentence]
- [Fourth important point - complete sentence]

ABSOLUTE REQUIREMENTS:

1. **SCRIPT PURITY**: 
   - Use ONLY {target_language} script from start to finish
   - NO mixing with other languages (no Hindi in Bengali, no Telugu in Kannada, etc.)
   - If you see any other script creeping in, STOP and restart
   - Numbers can use {target_language} native numerals if standard

2. **PROPER NOUNS**: 
   - Example: "Radhakrishnan" → correct phonetic form in {target_language} script
   - Transliterate places to {target_language}
   - Keep pronunciation similar to original

3. **ACRONYMS**: 
   - Keep UN, WHO, LADC, MDC in ENGLISH CAPITAL LETTERS
   - These are the ONLY allowed non-{target_language} characters

4. **COMPLETENESS**:
   - You MUST write ALL 4 bullet points completely
   - Each bullet should be 10-20 words
   - DO NOT stop writing until all 4 bullets are done
   - Total length: 120-160 words

5. **METADATA**:
   {"- Include: " + metadata_line if metadata_parts else "- Skip metadata line entirely"}
   {"- Keep Ref exactly as source" if has_ref else ""}
   {"- Translate only month names in dates" if has_date else ""}
   {"- Translate location to " + target_language if has_loc else ""}

6. **FORMATTING**:
   - Keep exact markdown: ##, ###, **, -
   - One line break between sections
   - Space after each bullet point dash

VERIFICATION CHECKLIST BEFORE SUBMITTING:
□ Used ONLY {target_language} script throughout (check every word!)
□ Wrote all 4 complete bullet points
□ Each bullet has 10-20 words
□ Metadata matches source structure
□ No mixed scripts from other languages

COMMON MISTAKES TO AVOID:
❌ Stopping after 2-3 bullets
❌ Mixing scripts (e.g., ধ্যান appearing in Marathi)
❌ Incomplete last bullet point
❌ Translating acronyms
❌ Too short bullet points (under 10 words)

OUTPUT (complete translation):"""


def get_Announcement_title_prompt(original: Announcement, target_language: str) -> str:
    return f"""Translate this title to {target_language}.

ORIGINAL: {original['title']}

CONTEXT: {original.get('content', '')[:200]}

RULES:
1. Use ONLY {target_language} script (no mixing with other languages)
2. Length: 40-100 characters
3. Format: [Who] + [Action Verb] + [What/Where]
4. Transliterate names/places to {target_language} script
5. Keep acronyms unchanged (UN, WHO, LADC, MDC)

QUALITY CHECK:
- Is it clear what happened?
- Is it in pure {target_language} script?
- Is the action verb prominent?
- Is it 40-100 characters?

GOOD EXAMPLES:
English: "VP Radhakrishnan Attends World Meditation Day in Telangana"
Telugu: "ఉపరాష్ట్రపతి తెలంగాణలో ప్రపంచ ధ్యాన దినోత్సవంలో పాల్గొన్నారు"
Hindi: "उपराष्ट्रपति ने तेलंगाना में विश्व ध्यान दिवस में भाग लिया"

OUTPUT (title only, pure {target_language} script):"""


def get_Announcement_description_prompt(content: str, target_language: str) -> str:
    return f"""Write ONE sentence summarizing this announcement in {target_language}.

CONTENT:
{content[:400]}

REQUIREMENTS:
1. Exactly ONE sentence (25-45 words)
2. Use ONLY {target_language} script (absolutely no mixing!)
3. Include: who, what, when, where, why
4. Transliterate names/places to {target_language} script
5. Keep acronyms unchanged
6. End with proper punctuation: । (Indic) or . (others)

STRUCTURE: [Who] + [did what] + [when] + [where] + [why/purpose]

EXAMPLE (Telugu):
"ఉపరాష్ట్రపతి సి.పి. రాధాకృష్ణన్ డిసెంబర్ 21, 2025న తెలంగాణలోని కాన్హా శాంతి వనంలో మొదటి ప్రపంచ ధ్యాన దినోత్సవాన్ని ప్రారంభించారు, ఇది ప్రపంచవ్యాప్తంగా ధ్యానాన్ని ప్రోత్సహించే UN గుర్తింపు పొందిన దినం."

VERIFY:
□ Only ONE sentence
□ Pure {target_language} script (no other languages!)
□ 25-45 words
□ Includes all key details

OUTPUT (one sentence only):"""


def get_Announcement_state_prompt(original: Announcement, target_language: str) -> str:
    state_translations = {
        "Telangana": {
            "Hindi": "तेलंगाना",
            "Bengali": "তেলেঙ্গানা", 
            "Telugu": "తెలంగాణ",
            "Tamil": "தெலங்கானா",
            "Marathi": "तेलंगणा",
            "Kannada": "ತೆಲಂಗಾಣ",
            "Malayalam": "തെലങ്കാന",
            "Punjabi": "ਤੇਲੰਗਾਨਾ",
            "Gujarati": "તેલંગાણા",
            "Odia": "ତେଲେଙ୍ଗାନା"
        },
        "Maharashtra": {
            "Hindi": "महाराष्ट्र",
            "Bengali": "মহারাষ্ট্র",
            "Telugu": "మహారాష్ట్ర",
            "Tamil": "மகாராஷ்டிரா",
            "Marathi": "महाराष्ट्र",
            "Kannada": "ಮಹಾರಾಷ್ಟ್ರ",
            "Malayalam": "മഹാരാഷ്ട്ര",
            "Punjabi": "ਮਹਾਰਾਸ਼ਟਰ",
            "Gujarati": "મહારાષ્ટ્ર",
            "Odia": "ମହାରାଷ୍ଟ୍ର"
        },
        "West Bengal": {
            "Hindi": "पश्चिम बंगाल",
            "Bengali": "পশ্চিমবঙ্গ",
            "Telugu": "పశ్చిమ బెంగాల్",
            "Tamil": "மேற்கு வங்காளம்",
            "Marathi": "पश्चिम बंगाल",
            "Kannada": "ಪಶ್ಚಿಮ ಬಂಗಾಳ",
            "Malayalam": "പശ്ചിമ ബംഗാൾ",
            "Punjabi": "ਪੱਛਮੀ ਬੰਗਾਲ",
            "Gujarati": "પશ્ચિમ બંગાળ",
            "Odia": "ପଶ୍ଚିମ ବଙ୍ଗ"
        },
        "Tamil Nadu": {
            "Hindi": "तमिलनाडु",
            "Bengali": "তামিলনাড়ু",
            "Telugu": "తమిళనాడు",
            "Tamil": "தமிழ்நாடு",
            "Marathi": "तमिळनाडू",
            "Kannada": "ತಮಿಳುನಾಡು",
            "Malayalam": "തമിഴ്‌നാട്",
            "Punjabi": "ਤਮਿਲਨਾਡੂ",
            "Gujarati": "તમિલનાડુ",
            "Odia": "ତାମିଲନାଡୁ"
        }
    }
    
    govt_translations = {
        "Hindi": "भारत सरकार",
        "Bengali": "ভারত সরকার",
        "Telugu": "భారత ప్రభుత్వం",
        "Tamil": "இந்திய அரசு",
        "Marathi": "भारत सरकार",
        "Kannada": "ಭಾರತ ಸರ್ಕಾರ",
        "Malayalam": "ഇന്ത്യാ സർക്കാർ",
        "Punjabi": "ਭਾਰਤ ਸਰਕਾਰ",
        "Gujarati": "ભારત સરકાર",
        "Odia": "ଭାରତ ସରକାର",
        "English": "IndiaGovt"
    }
    
    input_state = original['state']
    
    # Check if we have a direct translation
    if input_state in state_translations and target_language in state_translations[input_state]:
        return state_translations[input_state][target_language]
    
    # Check if it's a government/central announcement
    if input_state in govt_translations.values() or input_state == "IndiaGovt" or "Government" in input_state:
        return govt_translations.get(target_language, "IndiaGovt")
    
    # Otherwise, provide translation prompt
    return f"""Translate this Indian state name to {target_language}: {input_state}

RULES:
- Use official {target_language} name
- Pure {target_language} script only
- If not a valid state, return: {govt_translations.get(target_language, 'IndiaGovt')}

OUTPUT (state name only):"""


