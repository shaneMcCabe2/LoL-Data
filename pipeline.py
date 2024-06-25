import os
import pandas as pd
import sqlite3

# Define the directory where the CSV files are located
data_dir = 'rawData'

# Initialize empty DataFrames for Players, Teams, and Champions
Players = pd.DataFrame()
Teams = pd.DataFrame()
Champions = pd.DataFrame()

# Loop through all CSV files in the data directory
for filename in os.listdir(data_dir):
    if filename.endswith('.csv'):
        # Determine the league, year, and split from filename
        league = filename[:3]
        year = filename[4:8]
        split = 'Spring' if 'Spring' in filename else 'Summer'

        # Read the CSV file into a DataFrame
        df = pd.read_csv(os.path.join(data_dir, filename))

        # Add the league, year and, split columns to the DataFrame
        df['League'] = league
        df['Year'] = year
        df['Split'] = split

        # Combine the data into the appropriate DataFrame based on the filename
        if 'Player' in filename:
            Players = pd.concat([Players, df], ignore_index=True)
        elif 'Team' in filename:
            Teams = pd.concat([Teams, df], ignore_index=True)
        elif 'Champion' in filename:
            Champions = pd.concat([Champions, df], ignore_index=True)

# Drop duplicate rows from Teams and Champions DataFrames
Teams = Teams.drop_duplicates()
Champions = Champions.drop_duplicates()

# Create a SQLite database connection
conn = sqlite3.connect('league_data.db')

# Export DataFrames to SQLite tables
Players.to_sql('Players', conn, if_exists='replace', index=False)
Teams.to_sql('Teams', conn, if_exists='replace', index=False)
Champions.to_sql('Champions', conn, if_exists='replace', index=False)

# Close the database connection
conn.close()

print('Data exported to SQLite database successfully.')