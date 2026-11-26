# How can player behavior and trend predict player retention?

## Datasets (/data/raw/):
- [tamber_steam-video-games](https://www.kaggle.com/datasets/tamber/steam-video-games) -- included in repo
- [rabieelkharoua_gaming-behavior](https://www.kaggle.com/datasets/rabieelkharoua/predict-online-gaming-behavior-dataset) -- included in repo
- [fronkongames_steam-games-dataset](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset) -- **NOT INCLUDED in repo due to file size**; need to download manually
- [steam_idx](https://steamidx.com/api-docs) -- used API to collect data; added to a database with sqlite

## Data Processing (/data/raw/ -> /scripts/ -> /data/processed):
Run from csp571-project-video_game_retention.
- `python -m scripts.process_tamber`
- `python -m scripts.process_rabieelkharoua`
- `python -m scripts.process_fronkongames` (to open up a smaller sample file for easier viewing, `python -m scripts.process_fronkongames --sample`)
- `python -m scripts.process_steamidx`

## Data Analyzing (/data/processed/):
Run from csp571-project-video_game_retention.
- `python -m scripts.analyze_fronkongames`
- `python -m scripts.analyze_steamidx_games`
- 'python -m scripts.analyze_steamidx_player_history'