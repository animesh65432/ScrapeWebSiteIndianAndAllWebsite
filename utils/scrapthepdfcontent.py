from app_types.govt_item import GovtItem
from .OcrScanpdfurl import scan_pdf_url
import asyncio

async def extract_text_from_pdf_bytes(items: list[GovtItem]):
    try:
        result_items = []
        pdf_tasks = []
        
     
        for item in items:
            if item.get("link"):
                result_items.append(item)
            elif item.get("pdf_link"):
                pdf_tasks.append((item, asyncio.create_task(scan_pdf_url(item["pdf_link"]))))
           
        
        if pdf_tasks:
            results = await asyncio.gather(
                *(task for _, task in pdf_tasks), 
                return_exceptions
            )
            
            for (item, _), text in zip(pdf_tasks, results):
                
                if isinstance(text, Exception) or not text or not text.strip():
                    continue
                
                item["content"] = text
                result_items.append(item)
        
        return result_items

    except Exception as e:
        print(f"extract_text_from_pdf_bytes error: {str(e)}")
        return items