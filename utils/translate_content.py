# utils/translate_content.py
from utils.call_cloudfree_api import call_cloudflare
import time

def translate_content(content: str, target_language: str, source_link: str = "") -> str:
    """
    Smart translation that handles ANY size content.
    """
    
    content_length = len(content)
    
    # SMALL: Translate directly (reduced from 15000 to 8000)
    if content_length < 8000:
        prompt = f"Translate to {target_language}:\n\n{content}"
        return call_cloudflare(prompt)
    
    # HUGE: Create summary only
    if content_length > 80000:
        print(f"   📚 Document too large ({content_length:,} chars). Creating summary...")
        prompt = f"""Summarize this in 400 words, then translate to {target_language}:

{content[:15000]}

Summary:"""
        summary = call_cloudflare(prompt)
        return f"[SUMMARY]\n\n{summary}\n\n[Full document: {source_link}]"
    
    # LARGE: Split into SMALLER chunks (changed from 10000 to 5000)
    chunk_size = 5000  # ← SMALLER CHUNKS
    chunks = []
    
    # Split content into chunks
    for i in range(0, len(content), chunk_size):
        chunk = content[i:i + chunk_size]
        chunks.append(chunk)
    
    print(f"   📄 Translating {len(chunks)} parts...")
    
    translated_parts = []
    for i, chunk in enumerate(chunks, 1):
        print(f"      Part {i}/{len(chunks)}...", end=" ")
        
        try:
            # SIMPLE prompt - just the text, no extra words
            prompt = f"Translate to {target_language}:\n\n{chunk}"
            
            translated = call_cloudflare(prompt, max_tokens=1500)
            translated_parts.append(translated)
            print("✓")
            
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            # If translation fails, keep original with note
            translated_parts.append(f"[Translation failed]\n{chunk}")
        
        # Wait between requests
        if i < len(chunks):
            time.sleep(1)
    
    return "\n\n".join(translated_parts)