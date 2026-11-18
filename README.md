# How can player behavior and trend predict player retention?

## Datasets (/data/raw/):
- [tamber_steam-video-games](https://www.kaggle.com/datasets/tamber/steam-video-games) -- included in repo
- [rabieelkharoua_gaming-behavior-dataset](https://www.kaggle.com/datasets/rabieelkharoua/predict-online-gaming-behavior-dataset) -- included in repo
- [fronkongames_steam-games-dataset](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset) -- **NOT INCLUDED in repo due to file size**; need to download manually
- [steamidx_live-data](https://steamidx.com/api-docs) -- data not retrieved yet

## Data Processing (/data/raw/ -> /scripts/ -> /data/processed):
Run from csp571-project-video_game_retention.
- `python -m scripts.process_tamber`
- `python -m scripts.process_rabieelkharoua`
- `python -m scripts.process_fronkongames` (to oepn up a smaller sample file, `python -m scripts.process_fronkongames --sample`)