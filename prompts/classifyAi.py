from app_types.govt_item import GovtItem
from typing import Union

def get_prompt(item: Union[GovtItem, dict, str]) -> str:
    if not isinstance(item, dict):
        print(f"WARNING: get_prompt received {type(item).__name__}, returning default")
        return "skip"
    
    title = str(item.get("title") or "").strip()
    content = str(item.get("content") or "").strip()
    
    if not title and not content:
        return "skip"
    
    content_text = content if content else "(content missing, classify based on title)"
    title_text = title if title else "(title missing, classify based on content)"
    
    prompt = f"""You are an expert classifier for INDIAN GOVERNMENT DOCUMENTS.

TASK: Classify into ONE category: "important" OR "skip"

Classify as "important" ONLY IF ALL conditions are met:

1. SOURCE CHECK - Must be official government document from:
   ✓ Central/State Government, Ministry, Department
   ✓ Commission, Authority, Board
   ✓ District offices (Collector, DM, DC)
   ✓ Governor/CM/PM offices
   ✓ Has official markers: "Government of", "Notification", "Order", "Circular", "G.O."

2. PUBLIC IMPACT CHECK - Must benefit citizens directly:
   ✓ Jobs/Recruitment/Vacancies/Bharti
   ✓ Scholarships/Fellowships/Financial Aid
   ✓ Subsidies/Welfare Schemes/Yojana
   ✓ Deadline Extensions (forms/applications/exams)
   ✓ Exam Results/Admit Cards/Admissions
   ✓ New Policies affecting public (tax, fees, rights)
   ✓ Disaster Alerts/Safety Warnings
   ✓ Public Service Launches
   ✓ Pension/PF/Salary updates
   ✓ Ration Card/Aadhaar/Certificate services

Classify as "skip" if:
   ✗ News media reporting/journalism
   ✗ Routine transfers/postings/appointments
   ✗ Minor tenders (< 5 crore)
   ✗ Internal office memos/circulars
   ✗ Meeting schedules/minutes
   ✗ Routine audit reports
   ✗ Speeches/statements without action items
   ✗ Acknowledgements/condolences

CRITICAL: Only return "important" if it's an OFFICIAL document that DIRECTLY HELPS citizens.

RESPOND WITH ONLY ONE WORD: "important" OR "skip"

------------------------------
TITLE: {title_text}
CONTENT: {content_text}
------------------------------
"""
    return prompt