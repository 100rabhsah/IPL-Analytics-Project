import pandas as pd

# Load the ball-by-ball dataset
ball_df = pd.read_csv("Data/processed/ipl_ball_by_ball.csv")

# Batting Stats
batting_stats = ball_df.groupby(["match_number", "batsman"]).agg(
    runs_scored=("runs_batsman", "sum"),
    balls_faced=("ball", "count"),  # Count valid deliveries faced
    fours=("runs_batsman", lambda x: (x == 4).sum()),
    sixes=("runs_batsman", lambda x: (x == 6).sum())
).reset_index()

# Strike Rate Calculation
batting_stats["strike_rate"] = batting_stats.apply(
    lambda row: (row["runs_scored"] / row["balls_faced"]) * 100 if row["balls_faced"] > 0 else 0, axis=1
)

# Bowling Stats
bowling_stats = ball_df.groupby(["match_number", "bowler"]).agg(
    balls_bowled=("ball", "count"),  # Count valid deliveries bowled
    runs_conceded=("runs_total", "sum"),
    wickets=("wicket", "sum")
).reset_index()

# Calculate Overs Correctly (Convert Balls into Overs)
bowling_stats["overs"] = bowling_stats["balls_bowled"] // 6 + (bowling_stats["balls_bowled"] % 6) / 10

# Fix Economy Calculation (Runs per Over)
bowling_stats["economy"] = bowling_stats.apply(
    lambda row: (row["runs_conceded"] / row["overs"]) if row["overs"] > 0 else 0, axis=1
)

# Merge Batting & Bowling Data
player_stats = pd.merge(
    batting_stats, bowling_stats,
    left_on=["match_number", "batsman"], right_on=["match_number", "bowler"], 
    how="outer"
)

# Fill NaN values with 0
player_stats.fillna(0, inplace=True)

# Save Processed Data
player_stats.to_csv("Data/processed/ipl_player_stats.csv", index=False)

print("✅ Fixed Player Stats File Generated!")
