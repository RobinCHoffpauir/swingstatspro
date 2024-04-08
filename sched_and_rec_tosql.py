# %% imports and dataframes
# -*- coding: utf-8 -*-
"""
team comparison analysis using pybaseball
drawing inspiration from the github docs/examples folder of the repo
@author: parlayking (RobinCHoffpauir)
"""

import pybaseball as pyb
from pybaseball import schedule_and_record as sch
pyb.cache.enable()
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
import sqlite3, pandas as pd
pd.set_option('future.no_silent_downcasting', True)
global years
years = [2024, 2023, 2022,2021]
global year
year = []
today = dt.now()



def save_to_sqlite(df, team_name, db_name):
    # Create a new SQLite database or connect to an existing one
    conn = sqlite3.connect(f"{db_name}")

    # Save the DataFrame to the SQLite database
    df.to_sql(team_name, conn, if_exists='replace', index=False)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def save_teams_to_single_db(dfs, db_name):
    # Create a new SQLite database or connect to an existing one
    conn = sqlite3.connect(f"{db_name}")

    for team_name, df in dfs.items():
        # Save the DataFrame to the SQLite database in a table named after the team
        df.to_sql(team_name, conn, if_exists='replace', index=False)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


## iterate through the teams and seasons to lookup and save to db
for time in years:
    year = (time)


    rockies = pyb.schedule_and_record   (year, 'COL')
    giants = pyb.schedule_and_record    (year, 'SFG')
    dodgers = pyb.schedule_and_record   (year, 'LAD')
    white_sox = pyb.    schedule_and_record(year, 'CHW')
    astros = pyb.schedule_and_record    (year, 'HOU')
    brewers = pyb.schedule_and_record   (year, 'MIL')
    rays = pyb.schedule_and_record  (year, 'TBR')
    red_sox = pyb.schedule_and_record   (year, 'BOS')
    d_backs = pyb.schedule_and_record   (year, 'ARI')
    tigers = pyb.schedule_and_record    (year, 'DET')
    guardians = pyb.    schedule_and_record(year, 'CLE')
    twins = pyb.schedule_and_record (year, 'MIN')
    reds = pyb.schedule_and_record  (year, 'CIN')
    orioles = pyb.schedule_and_record   (year, 'BAL')
    blue_jays = pyb.    schedule_and_record(year, 'TOR')
    nationals = pyb.    schedule_and_record(year, 'WSN')
    angels = pyb.schedule_and_record    (year, 'LAA')
    rangers = pyb.schedule_and_record   (year, 'TEX')
    athletics = pyb.    schedule_and_record(year, 'OAK')
    mariners = pyb.schedule_and_record  (year, 'SEA')
    cubs = pyb.schedule_and_record  (year, 'CHC')
    royals = pyb.schedule_and_record    (year, 'KCR')
    padres = pyb.schedule_and_record    (year, 'SDP')
    yankees = pyb.schedule_and_record   (year, 'NYY')
    mets = pyb.schedule_and_record  (year, 'NYM')
    braves = pyb.schedule_and_record    (year, 'ATL')
    marlins = pyb.schedule_and_record   (year, 'MIA')
    reds = pyb.schedule_and_record  (year, 'CIN')
    phillies = pyb.schedule_and_record  (year, 'PHI')
    cardinals = pyb.    schedule_and_record(year, 'STL')
    pirates = pyb.schedule_and_record   (year, 'PIT')

    divisions = {
        "AL East": {"Boston": red_sox, "New York": yankees, "Tampa Bay": rays,
                    "Toronto": blue_jays, "Baltimore": orioles},
        "AL Central": {"Cleveland": guardians, "Detroit": tigers,
                       "Chicago": white_sox, "Kansas City": royals,
                       "Minnesota": twins},
        "AL West": {"Los Angeles": angels, "Houston": astros, "Seattle": mariners,
                    "Texas": rangers, "Oakland": athletics},
        "NL East": {"Washington": nationals, "New York": mets, "Atlanta": braves,
                    "Miami": marlins, "Philadelphia": phillies},
        "NL Central": {"Chicago": cubs, "Milwaukee": brewers, "St.Louis": cardinals,
                       "Pittsburgh": pirates, "Cinncinnati": reds},
        "NL West": {"Los Angeles": dodgers, "Arizona": d_backs, "Colorado": rockies,
                    "San Diego": padres, "San Francisco": giants}
    }
    for teams in divisions.values():
        save_teams_to_single_db(teams, f'betting/data/databases/{year}_schedule_record.db')
#### the tables that are saved to the database are: 
"""

Boston
Tampa Bay
Toronto
Baltimore
Cleveland
Detroit
Kansas City
Minnesota
Houston
Seattle
Texas
Oakland
Washington
New York
Atlanta
Miami
Philadelphia
Chicago
Milwaukee
St.Louis
Pittsburgh
Cinncinnati
Los Angeles
Arizona
Colorado
San Diego
San Francisco
"""

