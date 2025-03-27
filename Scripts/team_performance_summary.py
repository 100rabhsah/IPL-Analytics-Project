import pandas as pd

# Load datasets
matches_df = pd.read_csv("Data/processed/ipl_matches.csv")
balls_df = pd.read_csv("Data/processed/ipl_ball_by_ball.csv")

# 🏏 **Total Runs Scored by each Team (Batting)**
runs_scored = balls_df.groupby("inning")["runs_total"].sum().reset_index()
runs_scored.columns = ["team", "total_runs_scored"]

# 🔥 **Total Wickets Taken by each Team (Bowling)**
wickets_taken = balls_df[balls_df["wicket"].notna()].groupby("inning")["wicket"].count().reset_index()
wickets_taken.columns = ["team", "total_wickets_taken"]

# 🎯 **Overs Bowled Calculation (Excluding Wides & No Balls)**
valid_balls = balls_df[~balls_df["wicket"].isna()]  # Remove invalid balls
valid_balls["over_ball"] = valid_balls["ball"] / 6  # Convert balls to overs
overs_bowled = valid_balls.groupby("inning")["over_ball"].sum().reset_index()
overs_bowled.columns = ["team", "overs_bowled"]

# 💰 **Total Runs Conceded by each Team**
runs_conceded = balls_df.groupby("inning")["runs_total"].sum().reset_index()
runs_conceded.columns = ["team", "total_runs_conceded"]

# 📊 **Bowling Economy Calculation**
economy = pd.merge(overs_bowled, runs_conceded, on="team", how="left")
economy["bowling_economy"] = economy["total_runs_conceded"] / economy["overs_bowled"]

# 📌 **Matches Played by each Team**
matches_played = pd.concat([matches_df["team_1"], matches_df["team_2"]]).value_counts().reset_index()
matches_played.columns = ["team", "total_matches_played"]

# 🏆 **Matches Won & Win Percentage**
matches_won = matches_df["winner"].value_counts().reset_index()
matches_won.columns = ["team", "total_wins"]
team_performance = pd.merge(matches_played, matches_won, on="team", how="left").fillna(0)
team_performance["win_percentage"] = (team_performance["total_wins"] / team_performance["total_matches_played"]) * 100

# 🔄 **Merge All Stats**
team_performance = team_performance.merge(runs_scored, on="team", how="left").fillna(0)
team_performance = team_performance.merge(wickets_taken, on="team", how="left").fillna(0)
team_performance = team_performance.merge(economy, on="team", how="left").fillna(0)

# 📝 **Save to CSV**
team_performance.to_csv("Data/processed/team_performance_summary.csv", index=False)

print("✅ Team performance summary generated successfully!")
