from app_types.govt_item import GovtItem
from .OcrScanpdfurl import scan_pdf_url
import asyncio

async def extract_text_from_pdf_bytes(items: list[GovtItem]):
    try:
        tasks = []

        for item in items:
            pdf_url = item.get("pdf_link")

            if pdf_url:
                tasks.append((item, asyncio.create_task(scan_pdf_url(pdf_url))))

        results = await asyncio.gather(*(task for _, task in tasks), return_exceptions=True)

       
        for (item, task), text in zip(tasks, results):
            if isinstance(text, Exception):
                print(f"PDF scan failed for {item.get('pdf_link')}: {text}")
                continue

            item["content"] = text or ""

        return items

    except Exception as e:
        print(f"extract_text_from_pdf_bytes error: {str(e)}")
        return items
