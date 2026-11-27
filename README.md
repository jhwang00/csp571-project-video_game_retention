# How can player behavior and trend predict player retention?

## Datasets (/data/raw/):
- [tamber_steam-video-games](https://www.kaggle.com/datasets/tamber/steam-video-games) -- included in repo
- [rabieelkharoua_gaming-behavior](https://www.kaggle.com/datasets/rabieelkharoua/predict-online-gaming-behavior-dataset) -- included in repo
- [fronkongames_steam-games-dataset](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset) -- **NOT INCLUDED in repo due to file size**; need to download manually
- [steam_idx](https://steamidx.com/api-docs) -- used API to collect data; added to a database with sqlite

## Data Processing (/data/raw/ -> /scripts/ -> /data/semi_processed):
Run from csp571-project-video_game_retention.
- `python -m scripts.process.process_tamber`
- `python -m scripts.process.process_rabieelkharoua`
- `python -m scripts.process.process_fronkongames` (to open up a smaller sample file for easier viewing, `python -m scripts.process.process_fronkongames --sample`)
- `python -m scripts.process.process_steamidx`

## Data Analyzing (/data/semi_processed/):
Run from csp571-project-video_game_retention.
- `python -m scripts.analyze.analyze_fronkongames`
- `python -m scripts.analyze.analyze_steamidx_games`
- `python -m scripts.analyze.analyze_steamidx_player_history`