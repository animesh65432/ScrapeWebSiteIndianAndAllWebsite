import asyncio
import re
import sys
from dataclasses import dataclass
from urllib.parse import urlparse

import httpx


MIN_SCORE = 1

BLOCKED_DOMAINS = [
    "careers360", "shiksha.com", "collegedunia", "getmyuni",
    "jagranjosh", "jagran.com", "bhaskar.com", "patrika.com",
    "zeenews", "abplive", "newsbytesapp", "entrancezone",
    "successcds", "thenewsminute", "indiatvnews", "amarujala",
    "livehindustan", "navbharattimes", "firstpost.com",
    "theprint.in", "thequint.com", "cache.careers360",
]

PREFERRED_DOMAINS = [
    "pib.gov.in", "pib.nic.in", "india.gov.in", ".nic.in", ".gov.in",
    "thehindu.com", "businessstandard.com",
    "economictimes.indiatimes.com", "timesofindia.indiatimes.com",
    "aninews.in", "ani.in", "ptinews.com", "pti.in",
    "narendramodi.in", "pmindia.gov.in", "vikaspedia.in",
]

STOP_WORDS = {
    "the", "and", "for", "with", "from", "that", "this",
    "are", "was", "has", "have", "will", "its", "into",
    "official", "ceremony", "photo", "government", "scheme",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


@dataclass
class DDGResult:
    image:  str
    title:  str = ""
    url:    str = ""
    width:  int = 0
    height: int = 0



def domain_of(url: str) -> str:
    try:
        return urlparse(url).hostname.lower()
    except Exception:
        return ""

def is_blocked(url: str) -> bool:
    host = domain_of(url)
    return any(b in host for b in BLOCKED_DOMAINS)

def domain_bonus(url: str) -> int:
    host = domain_of(url)
    return 3 if any(p in host for p in PREFERRED_DOMAINS) else 0

def extract_keywords(query: str) -> list[str]:
    return [w for w in query.lower().split() if len(w) > 2 and w not in STOP_WORDS]

def score(result: DDGResult, keywords: list[str]) -> int:
    if is_blocked(result.image) or is_blocked(result.url):
        return -999
    haystack      = f"{result.title} {result.url} {result.image}".lower()
    keyword_score = sum(1 for kw in keywords if kw in haystack)
    bonus         = domain_bonus(result.image) + domain_bonus(result.url)
    size_bonus    = 1 if result.width >= 800 else 0
    return keyword_score + bonus + size_bonus



async def get_vqd_token(client: httpx.AsyncClient, query: str) -> str:
    response = await client.get(
        "https://duckduckgo.com/",
        params={"q": query, "iax": "images", "ia": "images"},
        headers=HEADERS,
    )
    response.raise_for_status()
    match = re.search(r"vqd=([\d-]+)", response.text)
    if not match:
        raise ValueError("Could not extract DDG vqd token.")
    return match.group(1)


async def get_image_results(client: httpx.AsyncClient, query: str, token: str) -> list[DDGResult]:
    response = await client.get(
        "https://duckduckgo.com/i.js",
        params={"q": query, "vqd": token, "f": ",,,,,", "p": "1", "s": "0"},
        headers={**HEADERS, "Referer": "https://duckduckgo.com/", "Accept": "application/json"},
    )
    response.raise_for_status()
    return [
        DDGResult(
            image=r["image"],
            title=r.get("title", ""),
            url=r.get("url", ""),
            width=r.get("width", 0),
            height=r.get("height", 0),
        )
        for r in response.json().get("results", [])
        if r.get("image")
    ]


async def find_best_image(query: str) -> str | None:
    async with httpx.AsyncClient(timeout=15) as client:
        token   = await get_vqd_token(client, query)
        results = await get_image_results(client, query, token)

    if not results:
        return None

    keywords       = extract_keywords(query)
    ranked_results = sorted(results, key=lambda r: score(r, keywords), reverse=True)
    best           = ranked_results[0]
    best_score     = score(best, keywords)

    if best_score < MIN_SCORE:
        return None

    return best.image

