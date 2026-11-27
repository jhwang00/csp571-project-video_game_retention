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

import csv
import requests

import pandas as pd
from video_game_retention.config import PROJECT_ROOT

FAILED_IDS_PATH = (
    PROJECT_ROOT / "data" / "etc" / "steamidx_failed_ids.csv"
)

def get_failed_app_ids():
    if not FAILED_IDS_PATH.exists():
        return set()

    df = pd.read_csv(FAILED_IDS_PATH)
    return set(df["app_id"].astype(int))

def save_failed_app_id(app_id, status_code):
    file_exists = FAILED_IDS_PATH.exists()

    with open(FAILED_IDS_PATH, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["app_id", "status_code"])

        writer.writerow([app_id, status_code])

"""
Collect fetch games meta data and games player history then save to DB
"""
def collect_game(app_id):
    game = get_steam_game_details(app_id)
    save_game_detail(game)

    history = get_steam_player_history(app_id, range_="all")
    save_player_history(history)

    # print(f"Collected: {game['name']} ({app_id})")

    
fronkon_df = pd.read_csv(
PROJECT_ROOT / "data" / "processed" / "fronkongames_steam-games.csv"
)


if __name__ == "__main__":
    init_database()

    # unique fronkon ids
    fronkon_ids = set(fronkon_df["AppID"].dropna().astype(int))

    # Create a reproducible random order of all FronkonGames IDs
    shuffled_ids = (
        pd.Series(sorted(fronkon_ids))
        .sample(frac=1, random_state=42)
        .tolist()
    )

    # Check the latest SQLite database
    collected_ids = get_database_app_ids()
    failed_ids = get_failed_app_ids()
    excluded_ids = collected_ids | failed_ids
    # Select the next 500 uncollected games
    ids_to_collect = []

    for app_id in shuffled_ids:
        if app_id not in excluded_ids:
            ids_to_collect.append(app_id)

        if len(ids_to_collect) >= 500:
            break


    print(f"Total FronkonGames IDs: {len(fronkon_ids)}")
    print(f"Already in database: {len(fronkon_ids & collected_ids)}")
    print(f"New games to collect: {len(ids_to_collect)}")

    for app_id in ids_to_collect:
        try:
            collect_game(app_id)
        except requests.HTTPError as e:
            status_code = e.response.status_code

            if status_code == 404:
                save_failed_app_id(app_id, status_code)
                failed_ids.add(app_id)
                print(f"404 - Recorded unavailable game: {app_id}")

            elif status_code == 429:
                print("API rate limit reached. Stopping collection.")
                break

            else:
                print(f"HTTP error for {app_id}: {e}")

        except Exception as e:
            print(f"Failed to collect {app_id}: {e}")