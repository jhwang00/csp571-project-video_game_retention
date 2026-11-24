import requests

# import api config
from video_game_retention.config import (
    STEAM_INDEX_API_KEY,
    STEAM_INDEX_API_URL,
)

# Fetch games from steamidx API
def get_steam_game_details(app_id: int) -> dict:
    """
    Fetches game details from the Steam Index API for a given app_id.
    """

    # Check if the API key is set
    if not STEAM_INDEX_API_KEY:
        raise ValueError("STEAM_INDEX_API_KEY is not set in the environment variables.")

    # Make a GET request to the Steam Index API
    res = requests.get(
        f"{STEAM_INDEX_API_URL}/apps/{app_id}",
        headers={"Authorization": f"Bearer {STEAM_INDEX_API_KEY}"},
        timeout=30,
    )
    res.raise_for_status()

    # return json data
    return res.json()["data"]


# Fetch games player history from steamidx API
def get_steam_player_history(app_id: int, range_: str = "all") -> dict:
    """
    Fetch historical concurrent-player counts for a Steam game.
    """

    # Check if API key is set
    if not STEAM_INDEX_API_KEY:
        raise ValueError("STEAM_INDEX_API_KEY is not configured.")

    # Maka a GET request of player data
    res = requests.get(
        f"{STEAM_INDEX_API_URL}/apps/{app_id}/players",
        headers={"Authorization": f"Bearer {STEAM_INDEX_API_KEY}"},
        params={"range": range_},
        timeout=30,
    )

    res.raise_for_status()

    return res.json()["data"]

# Request a batch of most played games from SteamIDX. Current limit is 500 - 700 games.
# Need to implement start at for expansion
def get_top_games(limit: int = 100):

    if not STEAM_INDEX_API_KEY:
        raise ValueError("STEAM_INDEX_API_KEY is not configured.")

    games = []
    cursor = None

    while len(games) < limit:
        page_size = min(100, limit - len(games))

        params = {"limit": page_size}
        
        if cursor is not None:
            params["cursor"] = cursor

        # make a request of 100 apps at a time, create new page for the remaining and repeat
        res = requests.get(
            f"{STEAM_INDEX_API_URL}/charts/most-played",
            headers={"Authorization": f"Bearer {STEAM_INDEX_API_KEY}"},
            params=params,
            timeout=30
        )

        res.raise_for_status()
        result = res.json()

        # extends because we want to add all element not the whole list
        games.extend(result["data"])

        cursor = result.get("meta", {}).get("nextCursor")

        if not cursor or not result["data"]:
            break

    return games
