from typing import Union, Dict

def get_prompt(item: Union[Dict, dict]) -> str:
    if not isinstance(item, dict):
        return "news"
    
    title = str(item.get("title") or "").strip()
    content = str(item.get("content") or "").strip()
    department = str(item.get("department") or "").strip()
    
    if not title and not content:
        return "news"
    
    # Use more content for better classification
    if content:
        content = content[:200]
    
    # Build input
    parts = []
    if title:
        parts.append(f"Title: {title}")
    if content:
        parts.append(f"Content: {content}")
    if department:
        parts.append(f"Source: {department}")
    
    text = "\n".join(parts)
    
    return f"""{text}

Question: Is this an Announcement or News?

Announcement = Citizens can take action NOW:
- Someone can apply for a job, exam, scholarship, or scheme
- There is a registration deadline or submission date
- People can bid on tenders or contracts
- Eligible citizens can enroll or participate in something
- There are specific steps to take (apply, register, submit documents)

News = No citizen action required:
- Government officials met, spoke, or visited somewhere
- A project was inaugurated or foundation stone was laid
- Policy was discussed or a report was released
- A cultural day, festival, or observance is being marked
- Training was completed or awards were given
- General information about programs (without how to apply)

Test: Ask "Can I personally do something specific because of this information RIGHT NOW?"
- YES with deadline/steps = announcement
- NO or just general info = news

Answer ONLY with one word: announcement or news

Answer:"""
def get_prompt(item: Union[Dict, dict]) -> str:
    if not isinstance(item, dict):
        return "news"
    
    title = str(item.get("title") or "").strip()
    content = str(item.get("content") or "").strip()
    department = str(item.get("department") or "").strip()
    
    if not title and not content:
        return "news"
    
    # Use more content for better classification
    if content:
        content = content[:300]  # Increased for better context
    
    # Build input
    parts = []
    if title:
        parts.append(f"Title: {title}")
    if content:
        parts.append(f"Content: {content}")
    if department:
        parts.append(f"Department: {department}")
    
    text = "\n".join(parts)
    
    return f"""{text}

---

Classify as "announcement" or "news":

ANNOUNCEMENT = Information that DIRECTLY AFFECTS citizens or requires awareness for compliance/benefit:

ACTION REQUIRED:
- Applications/registrations (jobs, exams, schemes, licenses, admissions)
- Tenders, bids, quotations
- Document submissions with deadlines
- Fee/tax payments before deadline

CITIZEN IMPACT (know this or face consequences):
- New rules/policies taking effect (traffic rules, regulations, GST rates)
- Service disruptions (water, electricity, road closures, transport changes)
- Price/tariff/fee changes
- Mandatory compliance deadlines (FASTag, documents, registrations)
- Public safety advisories (weather warnings, health alerts, security)
- Facility closures or timings changes

OPPORTUNITIES/BENEFITS:
- New services/facilities available (passport office, helpline, portal)
- Scheme benefits increased (pension, subsidy amounts)
- Results/selections published (exams, lotteries, beneficiary lists)
- Public consultations/hearings where citizens can participate
- Event registrations (camps, drives, workshops citizens can attend)

NEWS = Informational only, no direct citizen action or impact:

CEREMONIAL/ADMINISTRATIVE:
- Officials' meetings, visits, speeches
- Foundation stones laid, projects inaugurated
- Awards given, MOUs signed
- Cultural days/observances marked (International Year of X)
- Training programs completed by officials
- Reports released, policies discussed (not implemented)
- Government plans/proposals (not finalized)
- Statistics/data published (general information)
- Achievements/milestones celebrated

KEY TEST:
Ask: "Does this information require me to DO something, KNOW something for compliance, or am I AFFECTED by this?"
- YES (action/impact/affected) = announcement
- NO (just informational) = news

Answer ONLY: announcement or news

Answer:"""