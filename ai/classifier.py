from service.Groq import Groqclient
from app_types.govt_item import GovtItem
from prompts.classifyAi import get_prompt

async def classify_ai(item: GovtItem) -> str:
    """Async classification using AI"""
    
    # Validate input first
    if not isinstance(item, dict):
        print(f"WARNING: classify_ai received {item}")
        return "news"
    
    prompt = get_prompt(item)
    
    # If your Groq client supports async, use it
    # Check Groq documentation for async methods
    response = await Groqclient.chat.completions.create(  # Note: acreate for async
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=3,
        temperature=0
    )

    result = response.choices[0].message.content.strip().lower()

    print(f"classify_ai result: {result} for item title: {item.get('title', '')}")

    if result not in ["news", "announcement"]:
        result = "announcement"
    

    return result