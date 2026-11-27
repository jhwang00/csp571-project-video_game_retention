# execution: python -m scripts.process.process_tamber
# execution: python3 -m scripts.process.process_tamber

import pandas as pd

df = pd.read_csv(
    "data/raw/tamber_steam-video-games.csv",
    header=None,
    names=["UserID", "GameTitle", "Behavior", "Value", "Extra"]
)

rows_before = len(df)
shape_before = df.shape

# Remove unnecessary column
df = df.drop(columns=["Extra"])

# Remove invalid or missing records
df = df.dropna(subset=["UserID", "GameTitle", "Behavior", "Value"])

# Keep valid behaviors
df = df[df["Behavior"].isin(["purchase", "play"])]

# Remove invalid values
df = df[df["Value"] >= 0]

# Validate purchase values
df = df[
    ((df["Behavior"] == "purchase") & (df["Value"] == 1)) |
    (df["Behavior"] == "play")
]

# Find duplicate rows
duplicates = df[df.duplicated(keep=False)]
duplicates.to_csv(
    "data/etc/tamber_duplicates.csv",
    index=False
)

# Remove duplicates
df = df.drop_duplicates()

rows_after = len(df)
shape_after = df.shape

df.to_csv("data/semi_processed/tamber_steam-video-games.csv", index=False)

print("Rows before cleaning:", rows_before)
print("Rows after cleaning:", rows_after)
print("Rows removed:", rows_before - rows_after)
print("\nShape before cleaning:", shape_before)
print("Shape after cleaning:", shape_after)

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