import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

# Free, reliable Assam Govt & News RSS/Feeds (Zero API Cost)
FEEDS = [
    {"source": "Assam Govt & Recruitment News", "url": "https://news.google.com/rss/search?q=Assam+recruitment+2026+OR+NHM+Assam+OR+SLPRB+Assam&hl=en-IN&gl=IN&ceid=IN:en"},
    {"source": "Guwahati & Assam Walk-In / Jobs", "url": "https://news.google.com/rss/search?q=Guwahati+job+vacancy+OR+Assam+career+notification&hl=en-IN&gl=IN&ceid=IN:en"},
    {"source": "NE NOW Assam Career Feed", "url": "https://nenow.in/category/assam-career/feed"}
]

def fetch_feeds():
    collected = []
    seen_titles = set()

    for feed in FEEDS:
        try:
            req = urllib.request.Request(feed["url"], headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                xml_data = resp.read()
            root = ET.fromstring(xml_data)
            for item in root.findall(".//item")[:8]:
                title_el = item.find("title")
                link_el = item.find("link")
                pub_el = item.find("pubDate")
                if title_el is not None and link_el is not None:
                    title = title_el.text.strip()
                    if title.lower() not in seen_titles:
                        seen_titles.add(title.lower())
                        collected.append({
                            "title": title,
                            "link": link_el.text.strip(),
                            "source": feed["source"],
                            "summary": f"Fetched on {datetime.utcnow().strftime('%d %b %Y %H:%M UTC')} ({pub_el.text if pub_el is not None else 'Latest'})"
                        })
        except Exception as e:
            print(f"Skipping {feed['source']}: {e}")

    with open("data/scraped_inbox.json", "w", encoding="utf-8") as f:
        json.dump(collected[:20], f, indent=2, ensure_ascii=False)
    print(f"Saved {len(collected[:20])} Assam job alerts to data/scraped_inbox.json")

if __name__ == "__main__":
    fetch_feeds()
