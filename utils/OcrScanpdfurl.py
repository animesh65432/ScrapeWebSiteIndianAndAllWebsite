from config import config
import httpx, base64
import asyncio
from  utils.pdf_url_to_markdown import pdf_url_to_markdown

async def scan_pdf_url(url: str) -> str | None:
    try:
        print(f"🔍 Attempting to process: {url}")
        
        # Step 1: Try markdown conversion first
        mdtext = await pdf_url_to_markdown(url)
        if mdtext:
            print(f"✅ Markdown extraction successful for {url}")
            return mdtext
        
        print(f"⚠️ Markdown extraction failed, trying OCR for {url}")
        
        # Step 2: Download PDF
        async with httpx.AsyncClient(verify=False, timeout=120) as client:
            print(f"📥 Downloading PDF from {url}")
            response = await client.get(url)
            pdf_bytes = response.content
            print(f"📦 Downloaded {len(pdf_bytes)} bytes")

        if not pdf_bytes:
            print(f"❌ Failed to download PDF from {url}")
            return None

        # Step 3: Encode PDF to base64
        encoded_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        print(f"🔐 Encoded PDF to base64 ({len(encoded_pdf)} chars)")

        # Step 4: Send to Gemini API
        print(f"🤖 Sending to Gemini API...")
        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={config['GEMINI_API_KEY']}",
                json={
                    "contents": [
                        {
                            "parts": [
                                {
                                    "inlineData": {
                                        "mimeType": "application/pdf",
                                        "data": encoded_pdf
                                    }
                                },
                                {"text": "Extract all text from this scanned PDF clearly."}
                            ]
                        }
                    ]
                }
            )

        data = response.json()
        print(f"📨 Gemini response status: {response.status_code}")

        # Step 5: Safely extract text
        candidates = data.get("candidates", [])
        if not candidates:
            print(f"⚠️ No candidates in Gemini response for {url}")
            print(f"Response data: {data}")
            return None

        content = candidates[0].get("content", {})
        parts = content.get("parts", [])
        if not parts:
            print(f"⚠️ No parts in Gemini response for {url}")
            return None

        extracted_text = parts[0].get("text", "").strip()
        
        if extracted_text:
            print(f"✅ Extracted {len(extracted_text)} characters from {url}")
        else:
            print(f"⚠️ Empty text extracted from {url}")
        
        await asyncio.sleep(5)
        
        return extracted_text if extracted_text else None
        
    except Exception as e:
        print(f"❌ Exception in scan_pdf_url for {url}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None