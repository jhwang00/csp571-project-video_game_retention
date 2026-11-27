# execution: python -m scripts.analyze.analyze_fronkongames
# execution: python3 -m scripts.analyze.analyze_fronkongames

import csv
import pandas as pd
import argparse

file_path = "data/semi_processed/fronkongames_steam-games.csv"
with open(file_path, newline="") as file:
    reader = csv.reader(file)
    columns = next(reader)
df = pd.read_csv(file_path, low_memory=False, header=None, skiprows=1, names=columns)

print("\nColumn Summary:")
summary = pd.DataFrame({
    "Column": df.columns,
    "Exists": df.notna().sum().values,
    "Zeroes": df.eq(0).sum().values,
    "Total": len(df),
    "% Exists": (df.notna().sum() / len(df) * 100).round(2).values,
    "% Zero": (df.eq(0).sum() / len(df) * 100).round(2).values
})
print(summary.to_string(index=False))

categories = df["Categories"].dropna().str.split(",").explode().str.strip().unique()
genres = df["Genres"].dropna().str.split(",").explode().str.strip().unique()
tags = df["Tags"].dropna().str.split(",").explode().str.strip().unique()

category_counts = df["Categories"].dropna().str.split(",").explode().str.strip().value_counts()
genre_counts = df["Genres"].dropna().str.split(",").explode().str.strip().value_counts()
tag_counts = df["Tags"].dropna().str.split(",").explode().str.strip().value_counts()

print("\nCategory counts:")
print(category_counts.to_string(header=False))
print("\nGenre counts:")
print(genre_counts.to_string(header=False))
print("\nTag counts:")
print(tag_counts.to_string(header=False))
print("==========")
print("Unique categories:", len(categories))
print("Unique genres:", len(genres))
print("Unique tags:", len(tags))