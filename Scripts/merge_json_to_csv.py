import os
import json
import pandas as pd

# Paths
json_folder = "Data/raw/json_files"

# Lists to store data
matches = []
ball_by_ball = []

# Loop through each JSON file
for filename in os.listdir(json_folder):
    if filename.endswith(".json"):
        file_path = os.path.join(json_folder, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            # Extract match details
            match_info = data.get("info", {})
            match_id = match_info.get("event", {}).get("match_number")
            
            match_details = {
                "match_number": match_id,
                "season": match_info.get("dates", [None])[0][:4],  # Extract year from date
                "date": match_info.get("dates", [None])[0],
                "city": match_info.get("city"),
                "venue": match_info.get("venue"),
                "team_1": list(match_info.get("players", {}).keys())[0] if "players" in match_info else None,
                "team_2": list(match_info.get("players", {}).keys())[1] if "players" in match_info else None,
                "winner": match_info.get("outcome", {}).get("winner"),
                "win_by_runs": match_info.get("outcome", {}).get("by", {}).get("runs", 0),
                "win_by_wickets": match_info.get("outcome", {}).get("by", {}).get("wickets", 0),
                "player_of_match": match_info.get("player_of_match", [None])[0]
            }
            matches.append(match_details)

            # Extract ball-by-ball data
            for inning in data.get("innings", []):
                inning_name = inning.get("team")  # Batting team
                for over in inning.get("overs", []):
                    over_number = over.get("over")
                    for delivery in over.get("deliveries", []):
                        ball_details = {
                            "match_number": match_id,
                            "inning": inning_name,
                            "over": over_number,
                            "ball": delivery.get("ball"),
                            "batsman": delivery.get("batter"),
                            "bowler": delivery.get("bowler"),
                            "non_striker": delivery.get("non_striker"),
                            "runs_batsman": delivery.get("runs", {}).get("batter", 0),
                            "runs_extras": delivery.get("runs", {}).get("extras", 0),
                            "runs_total": delivery.get("runs", {}).get("total", 0),
                            "wicket": delivery.get("wickets", [{}])[0].get("kind") if delivery.get("wickets") else None,
                            "wicket_player": delivery.get("wickets", [{}])[0].get("player_out") if delivery.get("wickets") else None
                        }
                        ball_by_ball.append(ball_details)

# Convert to DataFrame & Save as CSV
df_matches = pd.DataFrame(matches)
df_matches.to_csv("Data/processed/ipl_matches.csv", index=False)

df_balls = pd.DataFrame(ball_by_ball)
df_balls.to_csv("Data/processed/ipl_ball_by_ball.csv", index=False)

print("✅ JSON files successfully merged into CSV!")
