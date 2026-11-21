from video_game_retention.api import (
    get_steam_game_details,
    get_steam_player_history,
    get_top_games
)
from video_game_retention.database import (
    init_database,
    save_game_detail,
    save_player_history,
    get_database_app_ids
)

"""
Collect fetch games meta data and games player history then save to DB
"""
def collect_game(app_id):
    game = get_steam_game_details(app_id)
    save_game_detail(game)

    history = get_steam_player_history(app_id, range_="all")
    save_player_history(history)

    # print(f"Collected: {game['name']} ({app_id})")


if __name__ == "__main__":
    init_database()

    top_games = get_top_games(500)

    app_ids = list(dict.fromkeys(
        game["appId"] for game in top_games
    ))

    collected_ids = get_database_app_ids()

    new_app_ids = []
    for app_id in app_ids:
        if app_id not in collected_ids:
            new_app_ids.append(app_id)

    print(f"Games retrieved: {len(app_ids)}")
    print(f"Already collected: {len(app_ids) - len(new_app_ids)}")
    print(f"New games to collect: {len(new_app_ids)}")

    for app_id in new_app_ids:
        try:
            collect_game(app_id)
        except Exception as e:
            print(f"Failed to collect {app_id}: {e}")