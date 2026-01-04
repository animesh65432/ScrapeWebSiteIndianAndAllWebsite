from typing import TypedDict

class Announcement(TypedDict):
    title: str
    content: str
    source_link: str
    date: str
    state: str
    originalAnnouncementId: str



def get_Announcement_summary_section_prompt(original: Announcement, target_language: str) -> str:
    """Generate summary section only"""
    
    has_ref = '**Ref:**' in original['content']
    has_date = '**Date:**' in original['content']
    has_loc = '**Loc:**' in original['content']
    
    metadata_parts = []
    if has_ref:
        metadata_parts.append("**Ref:** [exact value from source]")
    if has_date:
        metadata_parts.append("**Date:** [translate month only, keep numbers]")
    if has_loc:
        metadata_parts.append("**Loc:** [translate location]")
    
    metadata_line = " | ".join(metadata_parts)
    
    # Pre-compute the content prefix
    content_prefix = f"{metadata_line}\n\n" if metadata_parts else ""
    
    return f"""Create a summary section in {target_language}.

SOURCE:
{original['content']}

OUTPUT FORMAT (JSON):
{{
  "type": "summary",
  "heading": "[{target_language} word for 'Summary']",
  "content": "{content_prefix}[2-3 sentences: WHO did WHAT, WHEN, WHERE, WHY]"
}}

REQUIREMENTS:
- Use ONLY {target_language} script
- 40-60 words total
- Transliterate names/places to {target_language}
- Keep acronyms in ENGLISH (UN, WHO, etc.)
{f"- Start with metadata: {metadata_line}" if metadata_parts else ""}

OUTPUT (valid JSON only):"""

def get_Announcement_details_section_prompt(original: Announcement, target_language: str) -> str:
    """Generate details section only"""
    
    return f"""Create a details section in {target_language}.

SOURCE:
{original['content']}

OUTPUT FORMAT (JSON):
{{
  "type": "details",
  "heading": "[{target_language} word for 'Details']",
  "content": "[2-3 sentences with additional context, attendees, significance]"
}}

REQUIREMENTS:
- Use ONLY {target_language} script
- 40-60 words total
- Expand on context beyond summary
- Transliterate names/places to {target_language}
- Keep acronyms in ENGLISH (UN, WHO, etc.)

OUTPUT (valid JSON only):"""


def get_Announcement_keypoints_section_prompt(original: Announcement, target_language: str) -> str:
    """Generate key points section only"""
    
    return f"""Create a key points section in {target_language}.

SOURCE:
{original['content']}

OUTPUT FORMAT (JSON):
{{
  "type": "keypoints",
  "heading": "[{target_language} word for 'Key Information']",
  "points": [
    "[First point - complete sentence, 10-20 words]",
    "[Second point - complete sentence, 10-20 words]",
    "[Third point - complete sentence, 10-20 words]",
    "[Fourth point - complete sentence, 10-20 words]"
  ]
}}

REQUIREMENTS:
- Use ONLY {target_language} script
- Exactly 4 points (no more, no less)
- Each point: 10-20 words, complete sentence
- Transliterate names/places to {target_language}
- Keep acronyms in ENGLISH (UN, WHO, etc.)

CRITICAL: You MUST write all 4 points completely. Do NOT stop after 2-3 points!

OUTPUT (valid JSON only):"""


def get_Announcement_title_prompt(original: Announcement, target_language: str) -> str:
    return f"""You must translate this title to {target_language} language using SIMPLE, EASY words that a 5-year-old can understand.

IMPORTANT: Your output MUST be in {target_language} language, NOT in English (unless target language is English).

ORIGINAL: {original['title']}

CONTEXT: {original.get('content', '')[:200]}

TARGET LANGUAGE: {target_language}

RULES:
1. Write in {target_language} script ONLY (if target is Hindi, write in Devanagari; if Telugu, write in Telugu script; if Tamil, write in Tamil script, etc.)
2. Length: 40-100 characters
3. Use SIMPLE, COMMON words in {target_language} - avoid complex/technical terms
4. Format: [Who] + [Simple Action] + [What/Where]
5. Replace difficult words with easier alternatives in {target_language}
6. Keep acronyms unchanged (UN, WHO, LADC, MDC, PMMSY)

SIMPLIFICATION EXAMPLES:
❌ Complex: "inaugurated", "felicitated", "disseminated"
✅ Simple: "started", "honored", "shared"

❌ Complex: "constructed deep sea fishing vessels"
✅ Simple: "made big boats for fishing"

❌ Complex: "Standard Operation Procedure"
✅ Simple: "rules for how to work"

GOOD EXAMPLES FOR DIFFERENT LANGUAGES:
English Original: "Government Issues Standard Operation Procedure for Construction of Deep Sea Fishing Vessels"

If target is English:
✅ "Government Makes Rules for Building Big Fishing Boats"


CRITICAL INSTRUCTIONS - READ CAREFULLY:
- Your output MUST be written in {target_language} script
- DO NOT write in English if the target language is NOT English
- DO NOT write "Here is the translated title:" or "Here is:"
- DO NOT write "Let me know if this meets the requirements!"
- DO NOT write any introductory or closing phrases
- DO NOT add any explanations before or after
- Return ONLY the translated title text in {target_language}
- Start your response directly with the title in {target_language}
- just return the translated title text

WRONG OUTPUT EXAMPLES (DO NOT DO THIS):
❌ "Here is the translated title: [title]"
❌ "[title] Let me know if this meets the requirements!"
❌ "The translated title is: [title]"
❌ "Sure! Here's the translation: [title]"
❌ Writing in English when target is Hindi/Telugu/Tamil/etc.


CORRECT OUTPUT EXAMPLE :
✅ "Lakshadweep Administration Issues Corrigendum"

Remember: You are translating to {target_language}, so your entire response must be in {target_language} script!

OUTPUT:"""


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
7. Do NOT add any introductory or closing phrases
8. just return the summary sentence text

WRONG OUTPUT EXAMPLES (DO NOT DO THIS):
❌ "Here is the translated title: [title]"
❌ "[title] Let me know if this meets the requirements!"
❌ "The translated title is: [title]"
❌ "Sure! Here's the translation: [title]"
❌ Writing in English when target is Hindi/Telugu/Tamil/etc.

STRUCTURE: [Who] + [did what] + [when] + [where] + [why/purpose]

EXAMPLE :
"The Directorate of Social Welfare & Tribal Affairs, Lakshadweep Administration, has extended the last date for receipt of applications for the Best Performance Award for Persons with Disabilities 2025-26 to 05.01.2026. The extension was announced on 29.12.2025, revising the original deadline of 05.12.2025."

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


def get_Announcement_department_prompt(original: Announcement) -> str:
    """Extract department using STANDARDIZED list for consistency"""
    
    # Master list of standardized departments
    STANDARD_DEPARTMENTS = [
        # Information & Communication
        "DIPR",  # Department of Information & Public Relations
        "Department of Information Technology",
        
        # Constitutional Bodies
        "Election Commission of India",
        "State Election Commission",
        "UPSC",  # Union Public Service Commission
        "State Public Service Commission",
        
        # Chief Executive Offices
        "Prime Minister Office",
        "Chief Minister Office",
        "Lieutenant Governor Office",
        "Administrator Office",
        
        # Home & Internal Security
        "Ministry of Home Affairs",
        "State Home Department",
        "Police Department",
        "Disaster Management Authority",
        
        # Education & Culture
        "Ministry of Education",
        "State Education Department",
        "Ministry of Culture",
        "State Culture Department",
        "Ministry of Skill Development and Entrepreneurship",
        
        # Health & Family Welfare
        "Ministry of Health and Family Welfare",
        "State Health Department",
        "Ministry of AYUSH",
        
        # Finance & Economy
        "Ministry of Finance",
        "State Finance Department",
        "Reserve Bank of India",
        "State GST Department",
        "Income Tax Department",
        
        # Agriculture & Allied
        "Ministry of Agriculture and Farmers Welfare",
        "State Agriculture Department",
        "Ministry of Fisheries, Animal Husbandry and Dairying",
        "State Animal Husbandry Department",
        
        # Rural & Urban Development
        "Ministry of Rural Development",
        "State Rural Development Department",
        "Ministry of Panchayati Raj",
        "Ministry of Housing and Urban Affairs",
        "State Urban Development Department",
        
        # Social Welfare
        "Ministry of Women and Child Development",
        "State Women and Child Development Department",
        "Ministry of Social Justice and Empowerment",
        "State Social Welfare Department",
        "Ministry of Tribal Affairs",
        "State Tribal Welfare Department",
        "Ministry of Minority Affairs",
        
        # Labour & Employment
        "Ministry of Labour and Employment",
        "State Labour Department",
        "Employees' Provident Fund Organisation",
        
        # Infrastructure & Transport
        "Ministry of Road Transport and Highways",
        "State Transport Department",
        "Ministry of Railways",
        "Ministry of Civil Aviation",
        "Ministry of Ports, Shipping and Waterways",
        "State PWD",  # Public Works Department
        
        # Energy & Resources
        "Ministry of Power",
        "State Electricity Department",
        "Ministry of Coal",
        "Ministry of Petroleum and Natural Gas",
        "Ministry of New and Renewable Energy",
        
        # Industry & Commerce
        "Ministry of Commerce and Industry",
        "State Industries Department",
        "Ministry of Corporate Affairs",
        "Ministry of Micro, Small and Medium Enterprises",
        
        # Environment & Forest
        "Ministry of Environment, Forest and Climate Change",
        "State Forest Department",
        "Ministry of Jal Shakti",
        "State Water Resources Department",
        
        # Communication & Technology
        "Ministry of Communications",
        "Ministry of Electronics and Information Technology",
        "Department of Telecommunications",
        
        # Law & Justice
        "Ministry of Law and Justice",
        "State Law Department",
        "Supreme Court of India",
        "High Court",
        "District Court",
        
        # Defence & External Affairs
        "Ministry of Defence",
        "Ministry of External Affairs",
        
        # Food & Consumer Affairs
        "Ministry of Food Processing Industries",
        "Ministry of Consumer Affairs, Food and Public Distribution",
        "State Food and Civil Supplies Department",
        
        # Tourism & Aviation
        "Ministry of Tourism",
        "State Tourism Department",
        
        # Revenue & Land
        "State Revenue Department",
        "Land Records Department",
        
        # Administrative
        "District Administration",
        "Tehsil Office",
        "Block Development Office",
        "Municipal Corporation",
        "Municipal Council",
        "Gram Panchayat",
        
        # State Governments (All States)
        "Andhra Pradesh Government",
        "Arunachal Pradesh Government",
        "Assam Government",
        "Bihar Government",
        "Chhattisgarh Government",
        "Goa Government",
        "Gujarat Government",
        "Haryana Government",
        "Himachal Pradesh Government",
        "Jharkhand Government",
        "Karnataka Government",
        "Kerala Government",
        "Madhya Pradesh Government",
        "Maharashtra Government",
        "Manipur Government",
        "Meghalaya Government",
        "Mizoram Government",
        "Nagaland Government",
        "Odisha Government",
        "Punjab Government",
        "Rajasthan Government",
        "Sikkim Government",
        "Tamil Nadu Government",
        "Telangana Government",
        "Tripura Government",
        "Uttar Pradesh Government",
        "Uttarakhand Government",
        "West Bengal Government",
        
        # Union Territories
        "Andaman and Nicobar Islands Administration",
        "Chandigarh Administration",
        "Dadra and Nagar Haveli and Daman and Diu Administration",
        "Delhi Government",
        "Jammu and Kashmir Administration",
        "Ladakh Administration",
        "Lakshadweep Administration",
        "Puducherry Government",
        
        # Generic Categories
        "Central Government",
        "State Government",
        "Local Body",
        "Other"
    ]
    
    return f"""Identify the government department from this announcement.

TITLE: {original['title']}
CONTENT: {original['content'][:400]}
SOURCE URL: {original.get('source_link', '')}

STANDARDIZED DEPARTMENT LIST (choose EXACTLY ONE from this list):
{chr(10).join(f"- {dept}" for dept in STANDARD_DEPARTMENTS)}

MATCHING RULES:
1. If specific ministry/department mentioned, match to exact standard name
2. If URL contains identifier (e.g., "dipr.gov.in", "mha.gov.in"), use that
3. Match state-specific content to corresponding state government
4. Match central schemes/policies to relevant central ministry
5. If district/local announcement, use "District Administration" or specific local body
6. For state-level generic announcements without specific department, use "[State Name] Government"
7. For central-level generic announcements, use "Central Government"
8. Use "Other" only if absolutely no match found

EXAMPLES:
"Information & Public Relations Mizoram" → DIPR
"Ministry of Home Affairs circular" → Ministry of Home Affairs
"CM of Gujarat announces" → Chief Minister Office
"West Bengal Health Dept" → State Health Department
"Election Commission notice" → Election Commission of India
URL "pib.gov.in" → Central Government
"Guwahati Municipal Corporation" → Municipal Corporation
"PM's relief fund" → Prime Minister Office
"Karnataka Agriculture scheme" → State Agriculture Department
"Central GST notification" → Ministry of Finance

IMPORTANT: 
- Return EXACTLY as written in the standardized list
- Do NOT create new department names
- Do NOT combine or modify names
- Match to the CLOSEST and MOST SPECIFIC option
- Prefer specific department over generic state/central government

OUTPUT (department name only, must match list exactly):"""

def get_Announcement_category_prompt(original: Announcement) -> str:
    """Determine the category - returns single standardized word"""
    
    STANDARD_CATEGORIES = [
        "Election",
        "Scheme",
        "Award",
        "Policy",
        "Welfare",
        "Infrastructure",
        "Education",
        "Health",
        "Employment",
        "Agriculture",
        "Finance",
        "Event",
        "Notification",
        "Other"
    ]
    
    return f"""Analyze this announcement and choose ONE category.

TITLE: {original['title']}
CONTENT: {original['content'][:400]}

STANDARDIZED CATEGORY LIST (choose EXACTLY ONE from this list):
{chr(10).join(f"- {cat}" for cat in STANDARD_CATEGORIES)}

MATCHING RULES:
1. Choose the MOST SPECIFIC category that fits
2. If multiple categories apply, choose the PRIMARY one
3. Match based on main topic/purpose of announcement
4. Use "Other" only if absolutely no match found

CATEGORY DEFINITIONS:
- Election: Voting, election duty, results, schedules, polling, electoral process
- Scheme: Government programs, welfare schemes, subsidies, initiatives, yojanas
- Award: Honors, recognitions, prizes, ceremonies, felicitations, awards
- Policy: New rules, regulations, guidelines, acts, orders, government decisions
- Welfare: Social welfare, benefits, assistance, relief programs, aid
- Infrastructure: Roads, buildings, construction, development projects, public works
- Education: Schools, colleges, scholarships, exams, training, educational programs
- Health: Hospitals, medical services, health programs, vaccinations, healthcare
- Employment: Jobs, recruitment, hiring, employment programs, job fairs
- Agriculture: Farming, crops, irrigation, agricultural subsidies, farming schemes
- Finance: Budget, tax, economic policies, financial assistance, grants
- Event: Conferences, meetings, celebrations, inaugurations, functions
- Notification: General announcements, circulars, notices, public information
- Other: Anything that doesn't fit above categories

EXAMPLES:
"Election duty team arrives" → Election
"PM announces housing scheme" → Scheme
"State awards ceremony held" → Award
"New education policy released" → Policy
"CM inaugurates bridge" → Infrastructure
"Health camp organized" → Health

IMPORTANT:
- Return EXACTLY as written in the standardized list
- Do NOT create new category names
- Do NOT use variations or abbreviations
- Match to the CLOSEST option

OUTPUT (category name only, must match list exactly):"""