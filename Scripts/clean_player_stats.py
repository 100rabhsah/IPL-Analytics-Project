import pandas as pd

# Load player stats data
file_path = "Data/processed/ipl_player_stats.csv"
df = pd.read_csv(file_path)

# Remove invalid rows where 'batsman' or 'bowler' contains only numbers
df = df[df["batsman"].apply(lambda x: not str(x).isdigit())]
df = df[df["bowler"].apply(lambda x: not str(x).isdigit())]

# Remove leading numbers from 'bowler' names if present
df["bowler"] = df["bowler"].astype(str).apply(lambda x: " ".join(x.split()[1:]) if x.split()[0].isdigit() else x)

# Round numerical columns to 2 decimal places
df["strike_rate"] = df["strike_rate"].astype(float).round(2)
df["economy"] = df["economy"].astype(float).round(2)

# Save cleaned data
output_path = "Data/processed/player_stats_final.csv"
df.to_csv(output_path, index=False)

print("✅ Data cleaned and saved as player_stats_final.csv")
