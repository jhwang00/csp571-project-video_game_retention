import sqlite3, json

from video_game_retention.config import (
    DATABASE_PATH
)

def init_database():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DATABASE_PATH) as conn:
        conn.execute(
        """
        CREATE TABLE IF NOT EXISTS games (
                app_id INTEGER PRIMARY KEY,
                name TEXT,
                details_json TEXT,
                collected_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS player_history (
                app_id INTEGER NOT NULL,
                observed_at TEXT NOT NULL,
                players INTEGER,
                PRIMARY KEY (app_id, observed_at)
            )
        """)

def save_game_detail(game):
    with sqlite3.connect(DATABASE_PATH) as conn:
        conn.execute(
            """
            INSERT INTO games (app_id, name, details_json)
            VALUES (?, ?, ?)
            ON CONFLICT(app_id) DO UPDATE SET
                name = excluded.name,
                details_json = excluded.details_json,
                collected_at = CURRENT_TIMESTAMP
            """,
            (
                game['appId'],
                game["name"],
                json.dumps(game)
            )
        )

def save_player_history(history):
    rows = [
    (history["appId"], point["at"], point["players"])
    for point in history["points"]
    ]

    with sqlite3.connect(DATABASE_PATH) as conn:
        conn.executemany(
            """
            INSERT INTO player_history (app_id, observed_at, players)
            VALUES (?, ?, ?)
            ON CONFLICT(app_id, observed_at) DO UPDATE SET
                players = excluded.players
            """,
            rows,
            )

# execute returns a cursor object. fetchall() gets us a list of tuples (row), row[0] is the AppId we want
def get_database_app_ids():
    with sqlite3.connect(DATABASE_PATH) as conn:
        rows = conn.execute(
            """
            SELECT app_id
            FROM games
            WHERE app_id IN (
                SELECT DISTINCT app_id
                FROM player_history
            )
            """
        ).fetchall()

    return {row[0] for row in rows}
