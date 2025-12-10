from datetime import datetime
import json
from pathlib import Path


def save_to_json(announcements, region_name):
    """Save announcements to JSON with better error handling and logging"""
    
    # Create data directory
    data_dir = Path("data") / region_name
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{region_name}_{timestamp}.json"
    filepath = data_dir / filename
    
    # Save to JSON
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(announcements, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved {len(announcements)} announcements to {filepath}")
        
        return str(filepath)
        
    except Exception as e:
        print(f"❌ Error saving to JSON: {e}")
        return None