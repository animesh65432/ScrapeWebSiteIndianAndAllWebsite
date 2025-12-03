import json
from data import data  # your data list/dict

# Write JSON in human-readable Indian languages
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Data written to data.json with readable Indian languages!")
