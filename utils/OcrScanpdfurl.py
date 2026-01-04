from config import config
import httpx, base64
import asyncio
from utils.pdf_url_to_markdown import pdf_url_to_markdown

async def ocr_space_api(pdf_bytes: bytes) -> str | None:
    """OCR.space API - Free, no signup needed"""
    try:
        print("🔍 Using OCR.space API...")
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                "https://api.ocr.space/parse/image",
                files={"file": ("document.pdf", pdf_bytes, "application/pdf")},
                data={
                    "apikey": "helloworld",  # Free public key
                    "language": "eng",  # Auto-detects multiple languages
                    "isOverlayRequired": False,
                    "OCREngine": 2,  # Engine 2 better for non-Latin scripts
                    "detectOrientation": True,
                    "scale": True,
                    "isTable": True
                }
            )
            resp.raise_for_status()
            data = resp.json()
            
            if data.get('IsErroredOnProcessing'):
                error = data.get('ErrorMessage', ['Unknown error'])
                print(f"❌ OCR.space error: {error}")
                return None
            
            # Extract text from all pages
            all_text = []
            for idx, result in enumerate(data.get('ParsedResults', []), 1):
                text = result.get('ParsedText', '').strip()
                if text:
                    all_text.append(f"=== PAGE {idx} ===\n{text}")
            
            final_text = "\n\n".join(all_text)
            print(f"✅ OCR.space extracted {len(final_text)} characters")
            return final_text if final_text else None
            
    except Exception as e:
        print(f"❌ OCR.space error: {e}")
        return None


async def gemini_ocr(pdf_bytes: bytes, api_key: str) -> str | None:
    """Gemini API for OCR"""
    try:
        encoded_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        
        timeout = httpx.Timeout(connect=60.0, read=120.0, write=30.0, pool=30.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            print(f"🤖 Sending to Gemini...")
            resp = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}",
                json={
                    "contents": [{
                        "parts": [
                            {"inlineData": {"mimeType": "application/pdf", "data": encoded_pdf}},
                            {"text": "Extract all text from this PDF document clearly and completely."}
                        ]
                    }]
                }
            )
            resp.raise_for_status()
            data = resp.json()
        
        # Extract text
        candidates = data.get("candidates", [])
        if not candidates or not candidates[0].get("content", {}).get("parts"):
            print(f"⚠️ No Gemini content")
            return None
        
        extracted_text = candidates[0]["content"]["parts"][0].get("text", "").strip()
        print(f"✅ Gemini extracted {len(extracted_text)} chars")
        return extracted_text
        
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            print(f"⏰ Gemini rate limit hit (429)")
        else:
            print(f"❌ Gemini HTTP error {e.response.status_code}")
        return None
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return None


async def scan_pdf_url(url: str) -> str | None:
    """
    Extract text from PDF with multiple fallbacks:
    1. Markdown extraction (fastest)
    2. Gemini API (best quality)
    3. OCR.space API (free fallback)
    """
    pdf_bytes = None
    
    try:
        # Step 1: Try markdown extraction first
        print(f"🔍 Attempting to process: {url}")
        mdtext = await pdf_url_to_markdown(url)
        if mdtext and len(mdtext.strip()) > 100:
            print(f"✅ Markdown successful: {url}")
            return mdtext
        
        print(f"⚠️ Markdown failed, downloading PDF: {url}")
        
        # Step 2: Download PDF
        timeout = httpx.Timeout(connect=60.0, read=120.0, write=30.0, pool=30.0)
        async with httpx.AsyncClient(verify=False, timeout=timeout, limits=httpx.Limits(max_keepalive_connections=5)) as client:
            print(f"📥 Downloading: {url}")
            response = await client.get(url)
            response.raise_for_status()
            pdf_bytes = response.content
            print(f"📦 Downloaded {len(pdf_bytes):,} bytes")
        
        if not pdf_bytes:
            print(f"❌ No PDF data: {url}")
            return None
        
        # Check file size
        if len(pdf_bytes) > 20_000_000:  # 20MB limit
            print(f"❌ PDF too large ({len(pdf_bytes):,} bytes): {url}")
            return None
        
        # Step 3: Try Gemini API first (if available)
        gemini_key = config.get('GEMINI_API_KEY')
        if gemini_key and not gemini_key.startswith('sk-or-'):
            print(f"🤖 Trying Gemini OCR...")
            text = await gemini_ocr(pdf_bytes, gemini_key)
            if text and len(text.strip()) > 50:
                await asyncio.sleep(3)  # Rate limit
                return text
            print(f"⚠️ Gemini failed or returned empty, trying fallback...")
        
        # Step 4: Fallback to OCR.space (always free)
        print(f"🤖 Trying OCR.space (free fallback)...")
        text = await ocr_space_api(pdf_bytes)
        if text and len(text.strip()) > 50:
            await asyncio.sleep(2)  # Rate limit
            return text
        
        print(f"❌ All OCR methods failed: {url}")
        return None
        
    except httpx.ConnectTimeout:
        print(f"⏰ Connect timeout (slow server/network): {url}")
        return None
    except httpx.TimeoutException as e:
        print(f"⏰ Timeout: {str(e)} - {url}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP error {e.response.status_code}: {url}")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)} - {url}")
        import traceback
        traceback.print_exc()
        return None