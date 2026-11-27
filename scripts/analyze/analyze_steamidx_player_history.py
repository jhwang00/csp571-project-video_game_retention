# execution: python -m scripts.analyze.analyze_steamidx_player_history
# execution: python3 -m scripts.analyze.analyze_steamidx_player_history

import csv
import pandas as pd
import argparse

file_path = "data/semi_processed/steamidx_player_history.csv"
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

df["observed_at"] = pd.to_datetime(df["observed_at"]) # observed_at to datetime
app_summary = df.groupby("app_id").agg(
    DaysObserved=("observed_at", "nunique"),
    FirstObserved=("observed_at", "min"),
    LastObserved=("observed_at", "max")
).reset_index()

# calendar days between first/last observation
app_summary["CalendarDays"] = (
    app_summary["LastObserved"] - app_summary["FirstObserved"]
).dt.days + 1

# percentage of calendar days w/ observations
app_summary["ObservationPercentage"] = (
    app_summary["DaysObserved"] / app_summary["CalendarDays"] * 100
).round(2)

# remove time and rearrange columns
app_summary["FirstObserved"] = app_summary["FirstObserved"].dt.date
app_summary["LastObserved"] = app_summary["LastObserved"].dt.date
app_summary = app_summary[
    ["app_id", "DaysObserved", "CalendarDays",
     "ObservationPercentage", "FirstObserved", "LastObserved"]
]
print("\n", app_summary.to_string(index=False))

print("\nAverage observed:", round(app_summary["DaysObserved"].mean(), 2))
print("Shortest observed:", app_summary["DaysObserved"].min())
print("Longest observed:", app_summary["DaysObserved"].max())

print("\nObservation Coverage: ")
total_games = len(app_summary)
coverage_counts = {
    "< 7 observations": (app_summary["DaysObserved"] < 7).sum(),
    "> 7 observations": (app_summary["DaysObserved"] >= 7).sum(),
    "> 14 observations": (app_summary["DaysObserved"] >= 14).sum(),
    "> 30 observations": (app_summary["DaysObserved"] >= 30).sum(),
    "> 60 observations": (app_summary["DaysObserved"] >= 60).sum(),
    "---"
    "\n> 50% completeness": (app_summary["ObservationPercentage"] >= 50).sum(),
    "> 75% completeness": (app_summary["ObservationPercentage"] >= 75).sum(),
    "> 90% completeness": (app_summary["ObservationPercentage"] >= 90).sum(),
    "> 95% completeness": (app_summary["ObservationPercentage"] >= 95).sum(),
    "100% completeness": (app_summary["ObservationPercentage"] == 100).sum()
}
for label, count in coverage_counts.items():
    print(f"{label}: {count} / {total_games}")

print("\nPlayer Stats: ")
player_stats = df.groupby("app_id")["players"].agg(
    Mean="mean",
    Median="median",
    StdDev="std",
    Minimum="min",
    Maximum="max"
).reset_index()
print("Mean:", round(df["players"].mean(), 2))
print("Median:", round(df["players"].median(), 2))
print("Standard deviation:", round(df["players"].std(), 2))
print("Minimum:", df["players"].min())
print("Maximum:", df["players"].max())