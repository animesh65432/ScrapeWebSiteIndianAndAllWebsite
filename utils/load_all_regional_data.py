import json
import glob
from pathlib import Path

def load_all_regional_data(data_dir="data"):

    all_announcements = []

    json_files = glob.glob(f"data/{data_dir}/*.json", recursive=True)
    
    print(f"Found {json_files} JSON files")
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                if isinstance(data, list):
                    all_announcements.extend(data)
                elif isinstance(data, dict):
                    all_announcements.append(data)
                    
            print(f"✓ {Path(json_file).name}")
        except Exception as e:
            print(f"✗ {Path(json_file).name}: {e}")
    
    print(f"\nTotal: {len(all_announcements)} announcements")
    return all_announcements
