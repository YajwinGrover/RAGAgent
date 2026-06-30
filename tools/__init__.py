from tools.vector_tool import search_vector_db
from tools.bball_ref import (
    fetch_nba_player_stats,
    compare_position_stats_over_seasons,
    fetch_nba_team_stats,
    fetch_player_advanced_stats,
    fetch_player_career_stats,
    fetch_nba_standings,
    fetch_league_leaders,
    fetch_player_game_log,
)
from tools.news_tool import (
    search_sports_news,
    scrape_espn_headlines,
    search_reddit_nba,
    fetch_espn_nba_news,
    fetch_balldontlie_players,
    fetch_basketball_reference_history,
)


def get_all_tools():
    return [
        search_vector_db,
        fetch_nba_player_stats,
        compare_position_stats_over_seasons,
        fetch_nba_team_stats,
        fetch_player_advanced_stats,
        fetch_player_career_stats,
        fetch_nba_standings,
        fetch_league_leaders,
        fetch_player_game_log,
        search_sports_news,
        scrape_espn_headlines,
        search_reddit_nba,
        fetch_espn_nba_news,
        fetch_balldontlie_players,
        fetch_basketball_reference_history,
    ]
