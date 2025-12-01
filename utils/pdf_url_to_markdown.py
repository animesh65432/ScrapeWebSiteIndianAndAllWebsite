import asyncio
from concurrent.futures import ThreadPoolExecutor
import httpx
import fitz
import os


executor = ThreadPoolExecutor(max_workers=5)

def parse_pdf_blocking(file_path: str) -> str:
    doc = fitz.open(file_path)
    md = ""

    for i, page in enumerate(doc, 1):
        text = page.get_text("text").strip()

        md += f"## Page {i}\n\n"

        if text:
            # Normal PDF
            md += text + "\n\n"
        else:
            # Scanned PDF → show message AND extract images
            md += "> ⚠ Scanned page – no text layer available.\n\n"

            images = page.get_images(full=True)
            if not images:
                md += "> (No extractable images)\n\n"
            else:
                for img_index, img in enumerate(images, 1):
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    img_name = f"page{i}_img{img_index}.png"
                    pix.save(img_name)
                    md += f"![Scanned Image]({img_name})\n\n"

        md += "---\n\n"

    doc.close()
    return md



async def pdf_url_to_markdown(pdf_url: str, save_path: str = "temp.pdf",state:str="ArunachalPradesh") -> str:
    try:
        # Async download
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(pdf_url)
        
        if response.status_code != 200:
            raise ValueError(f"Failed to download PDF, status code {response.status_code}")
        
        # Async write to disk (offload blocking file write to thread pool)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(executor, lambda: open(save_path, "wb").write(response.content))
        
        # Parse PDF in thread pool (non-blocking for event loop)
        markdown_text = await loop.run_in_executor(executor, parse_pdf_blocking, save_path)
        
        # Delete PDF in thread pool
        await loop.run_in_executor(executor, lambda: os.remove(save_path))
        
        return markdown_text

    except Exception as e:
        if os.path.exists(save_path):
            await loop.run_in_executor(executor, lambda: os.remove(save_path))
        print(f"Error: {e}")
        return ""
