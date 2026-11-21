import os
from pathlib import Path

from dotenv import load_dotenv

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# loading the project enviroment
load_dotenv(PROJECT_ROOT / ".env")

# API Environment variables
STEAM_INDEX_API_KEY = os.getenv("STEAM_INDEX_API_KEY")
STEAM_INDEX_API_URL = "https://public-api.steamidx.com/v1"

# DB save path
DATABASE_PATH = PROJECT_ROOT / "data" / "processed" / "steam_games.db"