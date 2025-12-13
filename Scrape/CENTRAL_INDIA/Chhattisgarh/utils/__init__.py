from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from utils.fetch_with_httpx import fetch_with_httpx

async def scrape_website(url: str, days_back: int = 1):
    try:
        html = await fetch_with_httpx(url)

        if not html:
            print("Failed to fetch page")
            return []

        print(f"Page loaded successfully ({len(html)} bytes)")

        soup = BeautifulSoup(html, 'html.parser')

        print(soup)

        # Fix: Use proper BeautifulSoup syntax
        cards = soup.select(".col-lg-6.col-md-6.col-12")
        
        if not cards:
            print("⚠️  No notification cards found - check selector")
            return []

        results = []
        cutoff_date = (datetime.today() - timedelta(days=days_back)).date()

        for i, card in enumerate(cards, 1):
            try:
                # Extract date
                date_elem = card.select_one(".date p")
                if not date_elem:
                    print(f"Card {i}: No date found")
                    continue
                    
                date_text = date_elem.get_text(strip=True)
                date_obj = datetime.strptime(date_text, "%d %b, %Y").date()

                # Skip old notifications
                if date_obj < cutoff_date:
                    continue

                # Extract title
                title_elem = card.select_one(".notification-heading p")
                if not title_elem:
                    print(f"Card {i}: No title found")
                    continue
                    
                title = title_elem.get_text(strip=True)

                print(f"Card {i}: {title} | {date_obj}")

                # Extract PDF link
                link_elem = card.select_one(".notification-item")
                pdf_link = None

                if link_elem and link_elem.get('href'):
                    link = link_elem['href']
                    pdf_link = f"https://cgstate.gov.in{link}" if link.startswith("/") else link

                print(f"✅ Found: {title[:50]}... | {date_obj} | {pdf_link}")

                results.append({
                    "title": title,
                    "pdf_link": pdf_link,
                    "date": date_obj.isoformat(),
                    "state": "Chhattisgarh"
                })

            except ValueError as e:
                print(f"Card {i}: Date parsing error - {e}")
                continue
            except Exception as e:
                print(f"Card {i}: Processing error - {e}")
                continue

        print(f"\n📊 Total notifications found: {len(results)}")
        return results

    except Exception as e:
        print(f"❌ Scraping Error: {e}")
        import traceback
        traceback.print_exc()
        return []