"""tools/news_tool.py — Google News RSS + ESPN scraper + Reddit/BDL/BBRef"""

import os, time, textwrap, urllib.parse
import feedparser, requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool

_UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


@tool
def search_sports_news(query: str, limit: int | str = 6) -> str:
    """
    Search recent sports news via Google News RSS. No API key needed.
    Args:
        query: Search query e.g. 'NBA point guard scoring 2024'
        limit: Number of articles (1-10, default 6)
    Returns: Article titles, sources, dates, links.
    """
    limit = max(1, min(10, int(limit)))
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


@tool
def search_reddit_nba(query: str, limit: int | str = 5, time_filter: str = "month") -> str:
    """
    Search r/nba and r/nbadiscussion on Reddit for posts matching the query.
    Use for community opinions, trade rumors, game reactions, MVP debates.
    Args:
        query: Search query e.g. 'MVP race 2024', 'Luka Doncic trade'
        limit: Number of posts to return (1-10, default 5)
        time_filter: 'hour', 'day', 'week', 'month', 'year', 'all'
    Returns: Post titles, authors, and links from Reddit NBA communities.
    """
    limit = max(1, min(10, int(limit)))
    headers = {"User-Agent": "nba-agent-rss/1.0 (educational project)"}
    results = []
    for subreddit in ["nba", "nbadiscussion"]:
        url = (
            f"https://www.reddit.com/r/{subreddit}/search.rss"
            f"?q={urllib.parse.quote(query)}&sort=relevance&t={time_filter}&restrict_sr=on&limit={limit}"
        )
        try:
            feed = feedparser.parse(url, request_headers=headers)
            if getattr(feed, "status", 200) in (429, 403):
                continue
            for e in feed.entries[:limit]:
                results.append({
                    "subreddit": subreddit,
                    "title": e.get("title", ""),
                    "author": e.get("author", ""),
                    "published": e.get("published", ""),
                    "link": e.get("link", ""),
                })
        except Exception:
            continue
    if not results:
        return f"No Reddit posts found for '{query}' (Reddit may be rate-limiting — try again in a moment)."
    lines = [f"Reddit r/nba — '{query}'\n{'─'*50}"]
    for i, p in enumerate(results[:limit], 1):
        lines.append(
            f"{i:2}. [{p['subreddit']}] {p['title']}\n"
            f"     by {p['author']} | {p['published']}\n"
            f"     {p['link']}"
        )
    return "\n\n".join(lines)


@tool
def fetch_espn_nba_news(topic: str = "nba", limit: int | str = 8) -> str:
    """
    Get latest NBA news from ESPN via RSS feed. No API key needed.
    Use for breaking news, trade updates, injury reports, game recaps.
    Args:
        topic: Topic filter (currently 'nba' is the supported feed)
        limit: Number of articles (1-10, default 8)
    Returns: Article titles, descriptions, dates, and ESPN links.
    """
    limit = max(1, min(10, int(limit)))
    try:
        feed = feedparser.parse("https://www.espn.com/espn/rss/nba/news")
        if not feed.entries:
            return "No ESPN NBA news found."
        results = []
        for e in feed.entries[:limit]:
            summary = textwrap.shorten(
                BeautifulSoup(e.get("summary", ""), "html.parser").get_text(), 180, placeholder="…"
            )
            results.append(
                f"  {e.get('title', '')}\n"
                f"  {e.get('published', '')}\n"
                f"  {summary}\n"
                f"  {e.get('link', '')}"
            )
        return f"ESPN NBA News\n{'─'*50}\n\n" + "\n\n".join(results)
    except Exception as e:
        return f"ESPN RSS error: {e}"


@tool
def fetch_balldontlie_players(search: str) -> str:
    """
    Search for NBA player info from the Ball Don't Lie API.
    Returns player position, team, height, weight, jersey number.
    Requires BALLDONTLIE_API_KEY in .env — get a free key at https://app.balldontlie.io
    Args:
        search: Player name to search e.g. 'Nikola Jokic', 'LeBron James'
    Returns: Matching players with position, team, and physical attributes.
    """
    api_key = os.getenv("BALLDONTLIE_API_KEY", "")
    if not api_key:
        return (
            "Ball Don't Lie API requires an API key.\n"
            "Add BALLDONTLIE_API_KEY=your_key to your .env file.\n"
            "Get a free key at https://app.balldontlie.io"
        )
    try:
        r = requests.get(
            "https://api.balldontlie.io/v1/players",
            params={"search": search, "per_page": 10},
            headers={"Authorization": api_key},
            timeout=10,
        )
        if r.status_code == 401:
            return "Ball Don't Lie API: Unauthorized — check your BALLDONTLIE_API_KEY in .env."
        if r.status_code != 200:
            return f"Ball Don't Lie API error: HTTP {r.status_code}"
        data = r.json().get("data", [])
        if not data:
            return f"No players found for '{search}'."
        lines = [f"Ball Don't Lie — Players matching '{search}'\n{'─'*50}"]
        for p in data:
            team = p.get("team") or {}
            lines.append(
                f"  {p.get('first_name','')} {p.get('last_name','')}"
                f" | {p.get('position','?')}"
                f" | {team.get('full_name', '?')}"
                f" | Ht: {p.get('height','?')}"
                f" | Wt: {p.get('weight','?')} lbs"
                f" | Jersey: #{p.get('jersey_number','?')}"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Ball Don't Lie error: {e}"


@tool
def fetch_basketball_reference_history(player_name: str) -> str:
    """
    Get historical career stats from Basketball Reference. Best for retired players,
    historical comparisons, players not in current NBA API.
    Args:
        player_name: Player name e.g. 'Kobe Bryant', 'Michael Jordan', 'Larry Bird'
    Returns: Season-by-season per-game stats (G, MP, FG%, 3P%, FT%, TRB, AST, STL, BLK, PTS).
    """
    _UA_BBR = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    keep = {"Season", "Team", "G", "MP", "FG%", "3P", "3P%", "FT%", "TRB", "AST", "STL", "BLK", "TOV", "PTS"}
    try:
        time.sleep(2)
        search_url = (
            "https://www.basketball-reference.com/search/search.fcgi"
            f"?search={urllib.parse.quote(player_name)}"
        )
        r = requests.get(search_url, headers={"User-Agent": _UA_BBR}, timeout=15)
        if r.status_code in (429, 503):
            return "Basketball Reference unavailable (rate limited), try NBA API tools instead."
        if r.status_code != 200:
            return f"Basketball Reference unavailable (HTTP {r.status_code}), try NBA API tools instead."

        soup = BeautifulSoup(r.text, "html.parser")
        if "/players/" in r.url and "search" not in r.url:
            player_url = r.url
        else:
            items = soup.find_all("div", class_="search-item-name")
            player_href = next(
                (item.find("a")["href"] for item in items
                 if item.find("a") and "/players/" in item.find("a").get("href", "")),
                None,
            )
            if not player_href:
                return f"Player '{player_name}' not found on Basketball Reference."
            player_url = f"https://www.basketball-reference.com{player_href}"

        time.sleep(2)
        pr = requests.get(player_url, headers={"User-Agent": _UA_BBR}, timeout=15)
        if pr.status_code == 429:
            return "Basketball Reference unavailable (rate limited), try NBA API tools instead."
        if pr.status_code != 200:
            return f"Basketball Reference unavailable (HTTP {pr.status_code}), try NBA API tools instead."

        psoup = BeautifulSoup(pr.text, "html.parser")
        table = psoup.find("table", {"id": "per_game_stats"})
        if not table:
            return f"No career stats table found for '{player_name}' on Basketball Reference."

        thead_row = table.find("thead").find_all("tr")[-1]
        header = [th.get_text(strip=True) for th in thead_row.find_all("th")]
        col_indices = [i for i, h in enumerate(header) if h in keep]
        col_names = [header[i] for i in col_indices]

        rows = []
        for tr in table.find("tbody").find_all("tr"):
            if tr.has_attr("class") and "thead" in tr["class"]:
                continue
            cells = [td.get_text(strip=True) for td in tr.find_all(["th", "td"])]
            if not cells or not cells[0]:
                continue
            rows.append("  ".join(cells[i] if i < len(cells) else "" for i in col_indices))

        if not rows:
            return f"No season data found for '{player_name}'."

        return (
            f"{player_name} Career Stats (per game)\n"
            f"Source: basketball-reference.com\n{'─'*50}\n"
            + "  ".join(col_names) + "\n"
            + "\n".join(rows)
        )
    except Exception as e:
        return f"Basketball Reference unavailable, try NBA API tools instead. Error: {e}"
