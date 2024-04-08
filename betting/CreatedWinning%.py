# -*- coding: utf-8 -*-
"""
Created on Tue May 30 14:18:00 2023

@author: rhoffpauir
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 11 16:43:43 2023

@author: rhoffpauir
"""


import pandas as pd
from pybaseball import team_batting, team_pitching
from pybaseball.lahman import batting
import pybaseball as pyb
pyb.cache.enable()
import sqlite3

# replace the values for the divisions below with city : abbreviation key:value pairs



teams = ['BOS',
         'NYY',
         'TBR',
         'KCR',
         'CHW',
         'BAL',
         'CLE',
         'MIN',
         'DET',
         'HOU',
         'LAA',
         'SEA',
         'TEX',
         'OAK',
         'WSN',
         'MIA',
         'ATL',
         'NYM',
         'PHI',
         'CHC',
         'MIL',
         'STL',
         'PIT',
         'CIN',
         'LAD',
         'ARI',
         'COL',
         'SDP',
         'SFG',
         'TOR']
# delete all values from the dictionary, leaving just the keys
divisions = {
    "NL East" :{"WSN", "MIA", "ATL", "NYM", "PHI"},
    "NL Central" : {"CHC", "MIL", "STL", "PIT", "CIN"},
    "NL West" : {"LAD", "ARI", "COL", "SDP", "SFG"},
    "AL East" : {"TOR", "BOS", "CIN", "COL", "KCR"},
    "AL Central" : {"CLE", "DET", "CWS", "KCR", "MIN"},
    "AL West" : {"LAA", "HOU", "SEA", "TEX", "OAK"},
}


# Create the team_dfs dict needed to run script
global year
year = input("what year?: ")
team_batting_data = team_batting(year)
team_pitching_data = team_pitching(year)
##################
team_dfs = {}  # Create an empty #dictionary to store DataFrames #for each team
db_path = f"./data/databases/{year}_schedule_record.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()
team_dfs = {}
############################
for div in divisions:
    for team in divisions.get(div):
        c.execute(f"SELECT * FROM {team}")
        rows = c.fetchall()
        columns = [column[0] for column in c.description]
        team_dfs[team] = pd.DataFrame(rows, columns=columns)


# Merge the dataframes
team_data = pd.merge(team_batting_data[['Team', 'PA', 'R', 'wRC']], team_pitching_data[[
                     'Team', 'ER', 'IP', 'FIP']], on='Team')
runs, runs_allowed = team_batting_data[[
    'Team', 'R']], team_pitching_data[['Team', 'ER']]
run_data = pd.merge(runs, runs_allowed, on='Team')
# Calculate expected runs scored and allowed
team_data['Expected Runs Scored'] = team_data['wRC'] / team_data['IP']*9
team_data['Expected Runs Allowed'] = team_data['FIP']

# Calculate expected winning percentage
team_data['Created Winning %'] = team_data['Expected Runs Scored']**2 / \
    (team_data['Expected Runs Scored']**2 +
     team_data['Expected Runs Allowed']**2)
run_data['Pythag Expected %'] = run_data['R']**2 / \
    (run_data['R']**2 + run_data['ER']**2)
compare = pd.merge(run_data
[['Team', 'Pythag Expected %']], team_data[[
                   'Team', 'Created Winning %']], on='Team')

"""for team, df in team_dfs.items():
    # Determine wins: 1 for a win, 0 for a loss
    df['Win'] = df['Rslt'].apply(lambda x: 1 if x == 'W' else 0)

    # Calculate cumulative sum of wins
    df['Cumulative Wins'] = df['Win'].cumsum()

    # Calculate winning percentage: cumulative wins divided by number of games played so far
    df['Winning Percentage'] = df['Cumulative Wins'] / (df.index + 1)

compare.index = compare['Team']
compare = compare.drop('Team', axis=1)
for team in compare.index:
    z = team_dfs.get(team)['Winning Percentage']
    y = compare.loc[team]
    compare.loc[team, 'Win %'] = (z.iloc[161])
"""
print(compare)
