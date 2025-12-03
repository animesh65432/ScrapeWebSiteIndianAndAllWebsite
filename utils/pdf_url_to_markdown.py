import asyncio
from concurrent.futures import ThreadPoolExecutor
import httpx
import fitz
import os

executor = ThreadPoolExecutor(max_workers=5)

def save_file(path, data):
    with open(path, "wb") as f:
        f.write(data)

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)

def parse_pdf_blocking(file_path: str) -> str:
    doc = fitz.open(file_path)
    md = ""

    for i, page in enumerate(doc, 1):
        text = page.get_text("text").strip()

        if len(text) == 0:
            continue

        md += f"## Page {i}\n\n"

        if text:
            md += text + "\n\n"

        md += "---\n\n"

    doc.close()
    return md


async def pdf_url_to_markdown(pdf_url: str, save_path: str = "temp.pdf", state: str = "ArunachalPradesh") -> str:
    loop = asyncio.get_running_loop()

    try:
        # Download PDF asynchronously
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(pdf_url)

        if response.status_code != 200:
            raise ValueError(f"Failed to download PDF, status code {response.status_code}")

        # Save file (in thread)
        await loop.run_in_executor(executor, save_file, save_path, response.content)

        # Parse PDF (in thread)
        markdown_text = await loop.run_in_executor(executor, parse_pdf_blocking, save_path)

        # Delete file (in thread)
        await loop.run_in_executor(executor, delete_file, save_path)

        return markdown_text

    except Exception as e:
        await loop.run_in_executor(executor, delete_file, save_path)
        print(f"Error: {e}")
        return None
