import requests

# import api config
from video_game_retention.config import (
    STEAM_INDEX_API_KEY,
    STEAM_INDEX_API_URL,
)

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

def get_top_games(limit: int = 100) -> list[dict]:
    """
    Get the most played games from SteamIDX
    """

    if not STEAM_INDEX_API_KEY:
        raise ValueError("STEAM_INDEX_API_KEY is not configured.")

    res = requests.get(
        f"{STEAM_INDEX_API_URL}/charts/most-played",
        headers={"Authorization": f"Bearer {STEAM_INDEX_API_KEY}"},
        params={"limit":limit},
        timeout=30
    )

    res.raise_for_status()

    return res.json()["data"]
