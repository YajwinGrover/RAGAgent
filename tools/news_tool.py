"""tools/news_tool.py — Google News RSS + ESPN scraper"""

import textwrap, urllib.parse
import feedparser, requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool

_UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


@tool
def search_sports_news(query: str, limit: int = 6) -> str:
    """
    Search recent sports news via Google News RSS. No API key needed.
    Args:
        query: Search query e.g. 'NBA point guard scoring 2024'
        limit: Number of articles (1-10, default 6)
    Returns: Article titles, sources, dates, links.
    """
    limit = max(1, min(10, limit))
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query+' NBA')}&hl=en-US&gl=US&ceid=US:en"
    try:
        feed = feedparser.parse(url)
        if not feed.entries:
            return f"No news found for '{query}'."
        results = []
        for e in feed.entries[:limit]:
            summary = textwrap.shorten(BeautifulSoup(e.get("summary",""), "html.parser").get_text(), 180, placeholder="…")
            results.append(f"📰 {e.get('title','')}\n   {e.get('source',{}).get('title','Unknown')} | {e.get('published','')}\n   {summary}\n   {e.get('link','')}")
        return f"News — '{query}'\n{'─'*50}\n\n" + "\n\n".join(results)
    except Exception as e:
        return f"News error: {e}"


@tool
def scrape_espn_headlines(sport_path: str = "nba") -> str:
    """
    Scrape current ESPN headlines. Args: sport_path = 'nba', 'nfl', 'mlb', 'nhl'
    Returns: Latest ESPN story titles.
    """
    url = f"https://www.espn.com/{sport_path}/"
    try:
        soup = BeautifulSoup(requests.get(url, headers=_UA, timeout=15).text, "html.parser")
        headlines = [(t.get_text(strip=True), (t.find("a") or t.find_parent("a") or {}).get("href","")) for t in soup.select("h1,h2,h3") if len(t.get_text(strip=True)) > 20][:10]
        if not headlines:
            return "No ESPN headlines found."
        lines = [f"ESPN {sport_path.upper()} Headlines\n{'─'*50}"]
        for i, (title, link) in enumerate(headlines, 1):
            href = link if link.startswith("http") else f"https://www.espn.com{link}"
            lines.append(f"{i:2}. {title}\n     {href}")
        return "\n".join(lines)
    except Exception as e:
        return f"ESPN error: {e}"
