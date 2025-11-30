from typing import TypedDict, Optional

class GovtItem(TypedDict):
    title: Optional[str]
    content: Optional[str]
    link: Optional[str]
    pdf_link: Optional[str]
    department: Optional[str]
    state: str
