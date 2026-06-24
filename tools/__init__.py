from tools.vector_tool import search_vector_db
from tools.bball_ref import fetch_nba_player_stats, compare_position_stats_over_seasons
from tools.news_tool import search_sports_news, scrape_espn_headlines


def get_all_tools():
    return [
        search_vector_db,
        fetch_nba_player_stats,
        compare_position_stats_over_seasons,
        search_sports_news,
        scrape_espn_headlines,
    ]
