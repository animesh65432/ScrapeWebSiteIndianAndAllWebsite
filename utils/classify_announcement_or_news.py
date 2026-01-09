from typing import List
from app_types.govt_item import GovtItem
from ai.classifier import classify_ai
import asyncio

async def classify_announcement_or_news(
    items: List[GovtItem],
    max_concurrent: int = 30  
) -> List[GovtItem]:
    
    if not items:
        print("⚠️  No items to classify")
        return []
    
    classified_items = []
    news_items = []
    
    # Create semaphore for rate limiting
    semaphore = asyncio.Semaphore(max_concurrent)
    
    print(f"\n🚀 Starting classification of {len(items)} items...")
    print(f"⚙️  Max concurrent requests: {max_concurrent}")
    
    try:
        # Wrapper function with semaphore
        async def classify_with_semaphore(item: GovtItem) -> tuple:
            async with semaphore:
                result = await classify_ai(item)
                return item, result
        
        # Create tasks
        tasks = [classify_with_semaphore(item) for item in items]
        
        # Process with progress tracking
        completed = 0
        total = len(tasks)
        
        for coro in asyncio.as_completed(tasks):
            try:
                item, result = await coro
                
                if isinstance(result, Exception):
                    print(f"   ⚠️  Error: {item.get('title', 'Unknown')[:50]}")
                    news_items.append(item)  # Default to news on error
                elif result == "announcement":
                    classified_items.append(item)
                else:
                    news_items.append(item)
                
                completed += 1
                
                # Progress indicator every 50 items
                if completed % 50 == 0 or completed == total:
                    print(f"   Progress: {completed}/{total} ({completed/total*100:.1f}%)")
                    
            except Exception as e:
                print(f"   ❌ Unexpected error: {e}")
                completed += 1
        
        # Summary
        print(f"\n📊 Classification Summary:")
        print(f"   ✓ Announcements: {len(classified_items)}")
        print(f"   ✗ News (dropped): {len(news_items)}")
        print(f"   📈 Success rate: {len(classified_items)/len(items)*100:.1f}%")
        
        return classified_items
        
    except Exception as e:
        print(f"\n❌ Critical error in classify_announcement_or_news: {str(e)}")
        import traceback
        traceback.print_exc()
        return []