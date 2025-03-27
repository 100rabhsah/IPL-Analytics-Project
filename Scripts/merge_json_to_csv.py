import os
import json
import pandas as pd

# Path to folder containing all JSON files
json_folder = "Data/raw/json_files"

# List to store match data
matches = []

# Loop through each JSON file
for filename in os.listdir(json_folder):
    if filename.endswith(".json"):
        file_path = os.path.join(json_folder, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            # Extract match details from "info" section
            match_info = data.get("info", {})
            
            match_details = {
                "match_number": match_info.get("event", {}).get("match_number"),
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

# Convert to DataFrame & Save as CSV
df = pd.DataFrame(matches)
df.to_csv("Data/processed/ipl_matches.csv", index=False)

print("✅ JSON files successfully merged into CSV!")
