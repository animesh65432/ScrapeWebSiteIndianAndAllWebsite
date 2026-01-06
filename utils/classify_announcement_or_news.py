from typing import List
from app_types.govt_item import GovtItem
from ai.classifier import classify_ai
import asyncio

async def classify_announcement_or_news(items: List[GovtItem]) -> List[GovtItem]:
    classified_items = []
    news_items = [] 
    
    try:
        tasks = [classify_ai(item) for item in items]
        results = await asyncio.gather(*tasks, return_exceptions=True) 

        for item, item_type in zip(items, results):
            if item_type == "important":
                classified_items.append(item)
            else:
                news_items.append(item)  

      
        print(f"\n📊 Classification Summary:")
        print(f"✓ Announcements: {len(classified_items)}")
        print(f"✗ News (dropped): {len(news_items)}")

        return classified_items

    except Exception as e:
        print(f"classify_announcement_or_news_async error: {str(e)}")
        return []