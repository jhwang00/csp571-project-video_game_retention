# execution: python -m scripts.process_rabieelkharoua
# execution: python3 -m scripts.process_rabieelkharoua

import pandas as pd

df = pd.read_csv("data/raw/rabieelkharoua_gaming-behavior.csv")

rows_before = len(df)
shape_before = df.shape

# Remove duplicate records
df = df.drop_duplicates()

# Remove records missing important values
df = df.dropna()

# validations
df = df[df["Age"] >= 0]
df = df[df["PlayTimeHours"] >= 0]
df = df[df["InGamePurchases"].isin([0, 1])]
df = df[df["GameDifficulty"].isin(["Easy", "Medium", "Hard"])]
df = df[df["SessionsPerWeek"] >= 0]
df = df[df["AvgSessionDurationMinutes"] >= 0]
df = df[df["PlayerLevel"] >= 0]
df = df[df["AchievementsUnlocked"] >= 0]
df = df[df["EngagementLevel"].isin(["High", "Medium", "Low"])]

rows_after = len(df)
shape_after = df.shape

df.to_csv("data/processed/rabieelkharoua_gaming-behavior.csv", index=False)

print("Rows before cleaning:", rows_before)
print("Rows after cleaning:", rows_after)
print("Rows removed:", rows_before - rows_after)
print("\nShape before cleaning:", shape_before)
print("Shape after cleaning:", shape_after)