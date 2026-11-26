# execution: python -m scripts.process_steamidx
# execution: python3 -m scripts.process_steamidx

import pandas as pd
import json
import sqlite3

# Load SQLite database and read from it
conn = sqlite3.connect("data/raw/steam_idx.db")
games = pd.read_sql_query("SELECT * FROM games", conn)
player_history = pd.read_sql_query("SELECT * FROM player_history", conn)

conn.close()

details = games["details_json"].apply(json.loads)

# Extract selected fields into individual columns
games_clean = pd.DataFrame({
    "AppID": games["app_id"],
    "Name": games["name"],
    "ReleaseDate": details.apply(lambda x: x.get("releaseDate")),
    "IsFree": details.apply(lambda x: x.get("isFree")),
    "Developers": details.apply(lambda x: ",".join(x.get("developers", []))),
    "Publishers": details.apply(lambda x: ",".join(x.get("publishers", []))),
    "Franchises": details.apply(lambda x: ",".join(x.get("franchises", []))),
    "Genres": details.apply(lambda x: ",".join(x.get("genres", []))),
    "Categories": details.apply(lambda x: ",".join(x.get("categories", []))),
    "Tags": details.apply(lambda x: ",".join(tag.get("name", "") for tag in x.get("tags", []) if tag.get("name"))),
    "TotalReviews": details.apply(lambda x: x.get("reviews", {}).get("total")),
    "PositiveReviews": details.apply(lambda x: x.get("reviews", {}).get("positive")),
    "NegativeReviews": details.apply(lambda x: x.get("reviews", {}).get("negative")),
    "PositivePercent": details.apply(lambda x: x.get("reviews", {}).get("positivePercent")),
    "Summary": details.apply(lambda x: x.get("reviews", {}).get("summary")),
    "Rating": details.apply(lambda x: x.get("reviews", {}).get("rating")),
    "MetacriticScore": details.apply(lambda x: (x.get("metacritic") or {}).get("score")),
    "CurrentPlayers": details.apply(lambda x: x.get("players", {}).get("current")),
    "CurrentUpdatedAt": details.apply(lambda x: x.get("players", {}).get("updatedAt")),
    "AllTimePeak": details.apply(lambda x: x.get("players", {}).get("allTimePeak")),
    "AllTimePeakAt": details.apply(lambda x: x.get("players", {}).get("allTimePeakAt")),
    "GameUpdatedAt": details.apply(lambda x: x.get("updatedAt")),
})

# csv export
games_clean.to_csv("data/processed/steamidx_games.csv", index=False)
player_history.to_csv("data/processed/steamidx_player_history.csv", index=False)

print("Rows in games_clean:", len(games_clean))
print("Rows in player_history:", len(player_history))

