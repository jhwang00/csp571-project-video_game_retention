# execution: python -m scripts.process_fronkongames
# execution: python3 -m scripts.process_fronkongames
# optional: [--sample]

import csv
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--sample", action="store_true")
args = parser.parse_args()

# Read the original CSV header
file_path = "data/raw/fronkongames_steam-games.csv"
with open(file_path, newline="") as file:
    reader = csv.reader(file)
    columns = next(reader)

# Fix the merged column name
columns[7:8] = ["Discount", "DLC count"]

# Read the data using the corrected column names
df = pd.read_csv(file_path, low_memory=False, header=None, skiprows=1, names=columns)

rows_before = len(df)
shape_before = df.shape

# Columns to remove
drop_columns = [
    "About the game",
    "Supported languages",
    "Full audio languages",
    "Reviews",
    "Header image",
    "Website",
    "Support url",
    "Support email",
    "Windows",
    "Mac",
    "Linux",
    "Metacritic url",
    "Notes",
    "Screenshots",
    "Movies",
]
df = df.drop(columns=drop_columns)

# Remove duplicate games
df = df.drop_duplicates(subset=["AppID"])

# Find records missing essential identifiers
dropped_rows = df[df[["AppID", "Name"]].isna().any(axis=1)]
# Save dropped records separately
dropped_rows.to_csv("data/etc/fronkongames_missing.csv", index=False)
# Remove records without essential identifiers
df = df.dropna(subset=["AppID", "Name"])
print("Records missing identifiers:", len(dropped_rows))

rows_after = len(df)
shape_after = df.shape

if args.sample: # generate sample for easier viewing with --sample flag
    sample_df = df.sample(n=min(250, len(df)))
    sample_df.to_csv("data/processed/frokongames_sample.csv", index=False)

    print("Rows before cleaning:", rows_before)
    print("Sample rows:", len(sample_df))
else:
    df.to_csv("data/processed/fronkongames_steam-games.csv", index=False)

    print("Rows before cleaning:", rows_before)
    print("Rows after cleaning:", rows_after)
    print("Rows removed:", rows_before - rows_after)
    print("\nShape before cleaning:", shape_before)
    print("Shape after cleaning:", shape_after)

