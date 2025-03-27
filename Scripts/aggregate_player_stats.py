import pandas as pd

# Load the cleaned player stats data
file_path = "Data/processed/player_stats_final.csv"
df = pd.read_csv(file_path)

# Group by batsman to calculate batting performance
batting_summary = df.groupby("batsman").agg(
    total_runs=("runs_scored", "sum"),
    total_balls_faced=("balls_faced", "sum"),
    total_fours=("fours", "sum"),
    total_sixes=("sixes", "sum"),
)

# Calculate overall strike rate (Runs / Balls * 100)
batting_summary["strike_rate"] = (batting_summary["total_runs"] / batting_summary["total_balls_faced"]) * 100
batting_summary["strike_rate"] = batting_summary["strike_rate"].round(2)  # Round to 2 decimals

# Group by bowler to calculate bowling performance
bowling_summary = df.groupby("bowler").agg(
    total_balls_bowled=("balls_bowled", "sum"),
    total_runs_conceded=("runs_conceded", "sum"),
    total_wickets=("wickets", lambda x: x.count() if pd.notna(x).any() else 0),
)

# Convert balls to overs
bowling_summary["overs_bowled"] = (bowling_summary["total_balls_bowled"] // 6) + (bowling_summary["total_balls_bowled"] % 6) / 10

# Calculate economy rate (Runs Conceded / Overs)
bowling_summary["economy"] = bowling_summary["total_runs_conceded"] / (bowling_summary["total_balls_bowled"] / 6)
bowling_summary["economy"] = bowling_summary["economy"].round(2)

# Merge batting & bowling data
player_performance = pd.merge(
    batting_summary, bowling_summary, left_index=True, right_index=True, how="outer"
).fillna(0)  # Fill missing values with 0

# Save the summary
output_path = "Data/processed/player_performance_summary.csv"
player_performance.to_csv(output_path)

print("✅ Player performance summary saved as player_performance_summary.csv")
