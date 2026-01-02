from config import config
import httpx, base64
import asyncio
from  utils.pdf_url_to_markdown import pdf_url_to_markdown

async def scan_pdf_url(url: str) -> str | None:
    pdf_bytes = None
    try:
        print(f"🔍 Attempting to process: {url}")
        mdtext = await pdf_url_to_markdown(url)
        if mdtext:
            print(f"✅ Markdown successful: {url}")
            return mdtext
        
        print(f"⚠️ Markdown failed, trying OCR: {url}")
        
        # Fixed: Use client inside context with granular timeouts
        timeout = httpx.Timeout(connect=60.0, read=120.0, write=30.0)  # Longer connect for slow servers
        async with httpx.AsyncClient(verify=False, timeout=timeout, limits=httpx.Limits(max_keepalive_connections=5)) as client:
            print(f"📥 Downloading: {url}")
            response = await client.get(url)
            response.raise_for_status()  # Raises on 4xx/5xx
            pdf_bytes = response.content
            print(f"📦 Downloaded {len(pdf_bytes)} bytes")
        
        if not pdf_bytes:
            print(f"❌ No PDF data: {url}")
            return None
        
        # Base64 encode
        encoded_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        print(f"🔐 Encoded: {len(encoded_pdf)} chars")
        
        # Gemini with same timeout config
        async with httpx.AsyncClient(timeout=timeout) as client:
            print(f"🤖 Sending to Gemini...")
            resp = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={config['GEMINI_API_KEY']}",
                json={
                    "contents": [{"parts": [{"inlineData": {"mimeType": "application/pdf", "data": encoded_pdf}},
                                 {"text": "Extract all text from this scanned PDF clearly."}]}]
                }
            )
            resp.raise_for_status()
            data = resp.json()
        
        # Extract text (unchanged)
        candidates = data.get("candidates", [])
        if not candidates or not candidates[0].get("content", {}).get("parts"):
            print(f"⚠️ No Gemini content: {url}")
            return None
        extracted_text = candidates[0]["content"]["parts"][0].get("text", "").strip()
        
        print(f"✅ Extracted {len(extracted_text)} chars: {url}")
        await asyncio.sleep(5)  # Rate limit
        return extracted_text
        
    except httpx.ConnectTimeout:
        print(f"⏰ Connect timeout (slow server/network): {url}")
        return None
    except httpx.TimeoutException as e:
        print(f"⏰ Timeout: {str(e)} - {url}")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)} - {url}")
        import traceback
        traceback.print_exc()
        return None
