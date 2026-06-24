"""tools/bball_ref.py — NBA stats via nba_api"""

import time
import pandas as pd
from langchain_core.tools import tool

try:
    from nba_api.stats.endpoints import leaguedashplayerstats
    NBA_API_OK = True
except ImportError:
    NBA_API_OK = False


def _season(year: int) -> str:
    return f"{year - 1}-{str(year)[2:]}"


@tool
def fetch_nba_player_stats(position: str = "PG", season: int = 2024, stat_mode: str = "per_game") -> str:
    """
    Get NBA player stats from stats.nba.com for a position and season.
    Args:
        position: 'PG', 'SG', 'SF', 'PF', 'C', or 'ALL'
        season: Season end year e.g. 2024 = 2023-24
        stat_mode: 'per_game', 'totals', or 'per_36'
    Returns: Table of top 30 players.
    """
    if not NBA_API_OK:
        return "nba_api not installed. Run: pip install nba_api"
    mode = {"per_game": "PerGame", "totals": "Totals", "per_36": "Per36"}.get(stat_mode, "PerGame")
    try:
        time.sleep(0.6)
        df = leaguedashplayerstats.LeagueDashPlayerStats(
            season=_season(season), per_mode_detailed=mode, timeout=30
        ).get_data_frames()[0]
        if "GP" in df.columns:
            df = df[df["GP"] >= 20]
        pos_map = {"PG": "G", "SG": "G", "SF": "F", "PF": "F", "C": "C"}
        if position.upper() != "ALL" and "PLAYER_POSITION" in df.columns:
            df = df[df["PLAYER_POSITION"].str.contains(pos_map.get(position.upper(), position.upper()), na=False)]
        df = df.sort_values("PTS", ascending=False)
        cols = [c for c in ["PLAYER_NAME", "TEAM_ABBREVIATION", "GP", "PTS", "AST", "REB", "STL", "BLK", "FG_PCT", "FG3M"] if c in df.columns]
        return f"NBA {position} Stats — {_season(season)}\nSource: stats.nba.com\n{'─'*50}\n" + df[cols].head(30).to_string(index=False)
    except Exception as e:
        return f"NBA API error: {e}"


@tool
def compare_position_stats_over_seasons(position: str = "PG", start_season: int = 2015, end_season: int = 2024, stat_columns: str = "PTS,AST,REB,FG3M") -> str:
    """
    Compare average NBA stats for a position across multiple seasons. Great for trends and evolution analysis.
    Args:
        position: 'PG', 'SG', 'SF', 'PF', 'C'
        start_season: First season end year (e.g. 2015)
        end_season: Last season end year (e.g. 2024)
        stat_columns: Comma-separated stats e.g. 'PTS,AST,REB,FG3M'
    Returns: Season-by-season averages with % change.
    """
    if not NBA_API_OK:
        return "nba_api not installed."
    cols = [c.strip().upper() for c in stat_columns.split(",")]
    pos_map = {"PG": "G", "SG": "G", "SF": "F", "PF": "F", "C": "C"}
    api_pos = pos_map.get(position.upper(), position.upper())
    rows = []
    for yr in range(start_season, end_season + 1):
        try:
            time.sleep(0.8)
            df = leaguedashplayerstats.LeagueDashPlayerStats(season=_season(yr), per_mode_detailed="PerGame", timeout=30).get_data_frames()[0]
            if "PLAYER_POSITION" in df.columns:
                df = df[df["PLAYER_POSITION"].str.contains(api_pos, na=False)]
            if "GP" in df.columns:
                df = df[df["GP"] >= 20]
            row = {"Season": _season(yr)}
            for col in cols:
                row[col] = round(df[col].mean(), 2) if col in df.columns else "N/A"
            rows.append(row)
        except Exception:
            continue
    if not rows:
        return f"No data found for {position}."
    trend = pd.DataFrame(rows)
    pct = {"Season": "% Change"}
    for col in cols:
        if col in trend.columns and len(trend) >= 2:
            f = pd.to_numeric(trend[col].iloc[0], errors="coerce")
            l = pd.to_numeric(trend[col].iloc[-1], errors="coerce")
            pct[col] = f"{((l-f)/abs(f))*100:+.1f}%" if pd.notna(f) and f != 0 else "—"
    trend = pd.concat([trend, pd.DataFrame([pct])], ignore_index=True)
    return f"NBA {position} Averages — {_season(start_season)} to {_season(end_season)}\nSource: stats.nba.com\n{'─'*50}\n" + trend.to_string(index=False)
