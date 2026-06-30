"""tools/bball_ref.py — NBA stats via nba_api"""

import time
import pandas as pd
from langchain_core.tools import tool

try:
    from nba_api.stats.endpoints import (
        leaguedashplayerstats,
        leaguedashteamstats,
        playercareerstats,
        playerprofilev2,
        leaguestandingsv3,
        leagueleaders,
        playergamelog,
    )
    from nba_api.stats.static import players as static_players
    NBA_API_OK = True
except ImportError:
    NBA_API_OK = False


def _season(year: int) -> str:
    return f"{year - 1}-{str(year)[2:]}"


@tool
def fetch_nba_player_stats(position: str = "PG", season: int | str = 2024, stat_mode: str = "per_game", sort_by: str = "PTS") -> str:
    """
    Get NBA player stats from stats.nba.com for a position and season.
    Args:
        position: 'PG', 'SG', 'SF', 'PF', 'C', or 'ALL'
        season: Season end year e.g. 2024 = 2023-24
        stat_mode: 'per_game', 'totals', or 'per_36'
        sort_by: Column to sort by e.g. 'PTS', 'AST', 'REB', 'STL', 'BLK', 'FG3M'. Default 'PTS'.
    Returns: Top 20 players with MIN, PTS, AST, REB, STL, BLK, TOV, FG_PCT, FG3M, FG3_PCT, FT_PCT, PLUS_MINUS.
    """
    season = int(season)
    if not NBA_API_OK:
        return "nba_api not installed. Run: pip install nba_api"
    mode = {"per_game": "PerGame", "totals": "Totals", "per_36": "Per36"}.get(stat_mode, "PerGame")
    pos_map = {"PG": "G", "SG": "G", "SF": "F", "PF": "F", "C": "C"}
    api_pos = pos_map.get(position.upper(), "") if position.upper() != "ALL" else ""
    try:
        time.sleep(0.6)
        df = leaguedashplayerstats.LeagueDashPlayerStats(
            season=_season(season), per_mode_detailed=mode, timeout=30,
            player_position_abbreviation_nullable=api_pos,
        ).get_data_frames()[0]
        if "GP" in df.columns:
            df = df[df["GP"] >= 20]
        sort_col = sort_by.upper() if sort_by.upper() in df.columns else "PTS"
        df = df.sort_values(sort_col, ascending=False)
        cols = [c for c in ["PLAYER_NAME", "TEAM_ABBREVIATION", "GP", "MIN", "PTS", "AST", "REB", "STL", "BLK", "TOV", "FG_PCT", "FG3M", "FG3_PCT", "FT_PCT", "PLUS_MINUS"] if c in df.columns]
        return (
            f"NBA {position} Stats — {_season(season)} (sorted by {sort_col})\n"
            f"Source: stats.nba.com\n{'─'*50}\n"
            + df[cols].head(20).to_string(index=False)
        )
    except Exception as e:
        return f"NBA API error: {e}"


@tool
def compare_position_stats_over_seasons(position: str = "PG", start_season: int | str = 2015, end_season: int | str = 2024, stat_columns: str = "PTS,AST,REB,FG3M") -> str:
    """
    Compare average NBA stats for a position across multiple seasons. Great for trends and evolution analysis.
    Args:
        position: 'PG', 'SG', 'SF', 'PF', 'C'
        start_season: First season end year (e.g. 2015)
        end_season: Last season end year (e.g. 2024)
        stat_columns: Comma-separated stats. Available columns: PTS, AST, REB, STL, BLK, MIN,
            FGM, FGA, FG_PCT, FG3M, FG3A, FG3_PCT, FTM, FTA, FT_PCT, OREB, DREB, TOV, PLUS_MINUS.
            NOTE: PACE, USG_PCT, TS_PCT, EFG_PCT are NOT available in this endpoint.
    Returns: Season-by-season averages with % change.
    """
    start_season = int(start_season)
    end_season = int(end_season)
    if not NBA_API_OK:
        return "nba_api not installed."
    cols = [c.strip().upper() for c in stat_columns.split(",")]
    pos_map = {"PG": "G", "SG": "G", "SF": "F", "PF": "F", "C": "C"}
    api_pos = pos_map.get(position.upper(), "")
    rows = []
    for yr in range(start_season, end_season + 1):
        try:
            time.sleep(0.8)
            df = leaguedashplayerstats.LeagueDashPlayerStats(
                season=_season(yr), per_mode_detailed="PerGame", timeout=30,
                player_position_abbreviation_nullable=api_pos,
            ).get_data_frames()[0]
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


@tool
def fetch_nba_team_stats(season: int | str = 2024) -> str:
    """
    Get NBA team statistics for a season. Use for questions about best teams,
    offensive/defensive rankings, team comparisons, pace of play.
    Args:
        season: Season end year e.g. 2024 = 2023-24
    Returns: All 30 teams with W, L, PTS, AST, REB, OREB, DREB, STL, BLK, TOV, FG_PCT, FG3_PCT, PLUS_MINUS.
    """
    season = int(season)
    if not NBA_API_OK:
        return "nba_api not installed."
    try:
        time.sleep(0.6)
        df = leaguedashteamstats.LeagueDashTeamStats(
            season=_season(season), per_mode_detailed="PerGame", timeout=30
        ).get_data_frames()[0]
        df = df.sort_values("PTS", ascending=False)
        cols = [c for c in ["TEAM_NAME", "W", "L", "PTS", "AST", "REB", "OREB", "DREB", "STL", "BLK", "TOV", "FG_PCT", "FG3_PCT", "PLUS_MINUS"] if c in df.columns]
        return (
            f"NBA Team Stats — {_season(season)} (per game, sorted by PTS)\n"
            f"Source: stats.nba.com\n{'─'*50}\n"
            + df[cols].to_string(index=False)
        )
    except Exception as e:
        return f"NBA API error: {e}"


@tool
def fetch_player_advanced_stats(season: int | str = 2024, position: str = "ALL") -> str:
    """
    Get advanced NBA player metrics. Use for usage rate, true shooting percentage,
    efficiency, PIE score questions.
    Args:
        season: Season end year e.g. 2024 = 2023-24
        position: 'PG', 'SG', 'SF', 'PF', 'C', or 'ALL'
    Returns: Top 20 players by NET_RATING with USG_PCT, TS_PCT, AST_PCT, REB_PCT, NET_RATING, PIE.
    """
    season = int(season)
    if not NBA_API_OK:
        return "nba_api not installed."
    pos_map = {"PG": "G", "SG": "G", "SF": "F", "PF": "F", "C": "C"}
    api_pos = pos_map.get(position.upper(), "") if position.upper() != "ALL" else ""
    try:
        time.sleep(0.6)
        df = leaguedashplayerstats.LeagueDashPlayerStats(
            season=_season(season),
            measure_type_detailed_defense="Advanced",
            per_mode_detailed="PerGame",
            timeout=30,
            player_position_abbreviation_nullable=api_pos,
        ).get_data_frames()[0]
        if "GP" in df.columns:
            df = df[df["GP"] >= 20]
        df = df.sort_values("NET_RATING", ascending=False)
        cols = [c for c in ["PLAYER_NAME", "TEAM_ABBREVIATION", "USG_PCT", "TS_PCT", "AST_PCT", "REB_PCT", "NET_RATING", "PIE"] if c in df.columns]
        return (
            f"NBA Advanced Stats — {_season(season)} (sorted by NET_RATING)\n"
            f"Source: stats.nba.com\n{'─'*50}\n"
            + df[cols].head(20).to_string(index=False)
        )
    except Exception as e:
        return f"NBA API error: {e}"


def _find_player(player_name: str) -> dict | None:
    """Return first matching player dict (active preferred) or None."""
    hits = static_players.find_players_by_full_name(player_name)
    if not hits:
        hits = [p for p in static_players.get_players()
                if player_name.lower() in p["full_name"].lower()]
    if not hits:
        return None
    return next((p for p in hits if p.get("is_active")), hits[0])


@tool
def fetch_player_career_stats(player_name: str) -> str:
    """
    Get career season-by-season stats for a specific player by name. Use for career
    trajectory, player history, comparing two specific players over time.
    Args:
        player_name: Full or partial player name e.g. 'LeBron James', 'Stephen Curry'
    Returns: Season-by-season per-game stats with GP, PTS, AST, REB, STL, BLK, FG_PCT, FG3_PCT.
    """
    if not NBA_API_OK:
        return "nba_api not installed."
    player = _find_player(player_name)
    if not player:
        return f"Player not found: '{player_name}'. Check spelling."
    try:
        time.sleep(1.0)
        # playerprofilev2 is more reliable than playercareerstats for all player IDs
        df = playerprofilev2.PlayerProfileV2(
            player_id=player["id"], per_mode36="PerGame", timeout=30
        ).get_data_frames()[0]
        if df.empty:
            return f"No career data returned for {player['full_name']} (stats.nba.com unavailable — try again in a moment)."
        cols = [c for c in ["SEASON_ID", "TEAM_ABBREVIATION", "GP", "PTS", "AST", "REB", "STL", "BLK", "FG_PCT", "FG3_PCT"] if c in df.columns]
        return (
            f"{player['full_name']} Career Stats (per game)\n"
            f"Source: stats.nba.com\n{'─'*50}\n"
            + df[cols].to_string(index=False)
        )
    except Exception as e:
        return f"NBA API error: {e}"


@tool
def fetch_nba_standings(season: int | str = 2024) -> str:
    """
    Get current NBA standings by conference. Use for playoff picture,
    East vs West comparisons, win percentage questions.
    Args:
        season: Season end year e.g. 2024 = 2023-24
    Returns: All teams sorted by conference then wins, with W, L, WinPCT, HomeRecord, RoadRecord, L10, CurrentStreak.
    """
    season = int(season)
    if not NBA_API_OK:
        return "nba_api not installed."
    try:
        time.sleep(0.6)
        df = leaguestandingsv3.LeagueStandingsV3(
            season=_season(season), timeout=30
        ).get_data_frames()[0]
        df = df.sort_values(["Conference", "WINS"], ascending=[True, False])
        cols = [c for c in ["TeamCity", "TeamName", "Conference", "WINS", "LOSSES", "WinPCT", "HOME", "ROAD", "L10", "strCurrentStreak"] if c in df.columns]
        return (
            f"NBA Standings — {_season(season)}\n"
            f"Source: stats.nba.com\n{'─'*50}\n"
            + df[cols].to_string(index=False)
        )
    except Exception as e:
        return f"NBA API error: {e}"


@tool
def fetch_league_leaders(season: int | str = 2024, stat_category: str = "PTS", top_n: int | str = 10) -> str:
    """
    Get the top N players leading the league in a specific stat category.
    Use for who leads the league in any single statistic.
    Args:
        season: Season end year e.g. 2024 = 2023-24
        stat_category: One of PTS, AST, REB, STL, BLK, FG_PCT, FG3_PCT, EFF
        top_n: Number of players to return (default 10)
    Returns: Ranked list of top players for the requested stat.
    """
    season = int(season)
    top_n = int(top_n)
    if not NBA_API_OK:
        return "nba_api not installed."
    valid = {"PTS", "AST", "REB", "STL", "BLK", "FG_PCT", "FG3_PCT", "EFF"}
    stat = stat_category.upper()
    if stat not in valid:
        stat = "PTS"
    try:
        time.sleep(0.6)
        df = leagueleaders.LeagueLeaders(
            season=_season(season),
            stat_category_abbreviation=stat,
            per_mode48="PerGame",
            timeout=30,
        ).get_data_frames()[0]
        base_cols = [c for c in ["RANK", "PLAYER", "TEAM", "GP", stat] if c in df.columns]
        extra_cols = [c for c in ["PTS", "AST", "REB", "STL", "BLK"] if c in df.columns and c not in base_cols]
        cols = base_cols + extra_cols[:3]
        return (
            f"NBA League Leaders — {stat} — {_season(season)}\n"
            f"Source: stats.nba.com\n{'─'*50}\n"
            + df[cols].head(top_n).to_string(index=False)
        )
    except Exception as e:
        return f"NBA API error: {e}"


@tool
def fetch_player_game_log(player_name: str, season: int | str = 2024, last_n_games: int | str = 10) -> str:
    """
    Get recent game-by-game stats for a specific player. Use for recent form,
    hot streaks, last N games performance.
    Args:
        player_name: Full or partial player name e.g. 'Stephen Curry', 'LeBron James'
        season: Season end year e.g. 2024 = 2023-24
        last_n_games: How many recent games to return (default 10)
    Returns: Game-by-game log with GAME_DATE, MATCHUP, WL, PTS, AST, REB, STL, PLUS_MINUS.
    """
    season = int(season)
    last_n_games = int(last_n_games)
    if not NBA_API_OK:
        return "nba_api not installed."
    player = _find_player(player_name)
    if not player:
        return f"Player not found: '{player_name}'. Check spelling."
    try:
        time.sleep(0.6)
        df = playergamelog.PlayerGameLog(
            player_id=player["id"], season=_season(season), timeout=30
        ).get_data_frames()[0]
        cols = [c for c in ["GAME_DATE", "MATCHUP", "WL", "PTS", "AST", "REB", "STL", "PLUS_MINUS"] if c in df.columns]
        return (
            f"{player['full_name']} — Last {min(last_n_games, len(df))} Games ({_season(season)})\n"
            f"Source: stats.nba.com\n{'─'*50}\n"
            + df[cols].head(last_n_games).to_string(index=False)
        )
    except Exception as e:
        return f"NBA API error: {e}"
