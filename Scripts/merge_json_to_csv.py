import os
import json
import pandas as pd

# Paths
json_folder = "Data/raw/json_files"
output_folder = "Data/processed"

# Ensure output directory exists
os.makedirs(output_folder, exist_ok=True)

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
            match_id = match_info.get("event", {}).get("match_number", "Unknown")

            match_details = {
                "match_number": match_id,
                "season": match_info.get("dates", [None])[0][:4] if match_info.get("dates") else None,
                "date": match_info.get("dates", [None])[0] if match_info.get("dates") else None,
                "city": match_info.get("city", "Unknown"),
                "venue": match_info.get("venue", "Unknown"),
                "team_1": list(match_info.get("players", {}).keys())[0] if "players" in match_info and len(match_info["players"]) > 0 else None,
                "team_2": list(match_info.get("players", {}).keys())[1] if "players" in match_info and len(match_info["players"]) > 1 else None,
                "winner": match_info.get("outcome", {}).get("winner", "No Result"),
                "win_by_runs": match_info.get("outcome", {}).get("by", {}).get("runs", 0),
                "win_by_wickets": match_info.get("outcome", {}).get("by", {}).get("wickets", 0),
                "player_of_match": match_info.get("player_of_match", [None])[0]
            }
            matches.append(match_details)

            # Extract ball-by-ball data
            for inning in data.get("innings", []):
                inning_name = inning.get("team", "Unknown")  # Batting team
                for over in inning.get("overs", []):
                    over_number = over.get("over", 0)

                    for delivery_index, delivery in enumerate(over.get("deliveries", []), start=1):
                        ball_id = f"{over_number}.{delivery_index}"  # Construct correct ball number

                        ball_details = {
                            "match_number": match_id,
                            "inning": inning_name,
                            "ball": ball_id,
                            "batsman": delivery.get("batter", "Unknown"),
                            "bowler": delivery.get("bowler", "Unknown"),
                            "non_striker": delivery.get("non_striker", "Unknown"),
                            "runs_batsman": delivery.get("runs", {}).get("batter", 0),
                            "runs_extras": delivery.get("runs", {}).get("extras", 0),
                            "runs_total": delivery.get("runs", {}).get("total", 0),
                            "wicket": delivery["wickets"][0]["kind"] if "wickets" in delivery else None,
                            "wicket_player": delivery["wickets"][0]["player_out"] if "wickets" in delivery else None
                        }
                        ball_by_ball.append(ball_details)

# Convert to DataFrame & Save as CSV
df_matches = pd.DataFrame(matches)
df_matches.to_csv(os.path.join(output_folder, "ipl_matches.csv"), index=False)

df_balls = pd.DataFrame(ball_by_ball)
df_balls.to_csv(os.path.join(output_folder, "ipl_ball_by_ball.csv"), index=False)

print("✅ JSON files successfully merged into CSV!")
