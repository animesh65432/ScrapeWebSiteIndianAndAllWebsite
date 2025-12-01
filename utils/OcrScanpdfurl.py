from config import config
import httpx, base64

async def scan_pdf_url(url: str) -> str | None:
    try:
        # Step 1: Download PDF
        async with httpx.AsyncClient(verify=False, timeout=120) as client:
            response = await client.get(url)
            pdf_bytes = response.content

        if not pdf_bytes:
            print(f"Failed to download PDF from {url}")
            return None

        # Step 2: Encode PDF to base64
        encoded_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

        # Step 3: Send to Gemini API
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
        print("GEMINI RAW:", data)

        # Step 4: Safely extract text
        candidates = data.get("candidates", [])
        if not candidates:
            return None

        content = candidates[0].get("content", {})
        parts = content.get("parts", [])
        if not parts:
            return None

        extracted_text = parts[0].get("text", "").strip()
        return extracted_text if extracted_text else None

    except Exception as e:
        print(f"Error in scan_pdf_url: {e}")
        return None
