import datetime as dt
import sqlite3
import pandas as pd
import pybaseball as pyb
import matplotlib.pyplot as plt
import seaborn as sns
pyb.cache.enable()

today = dt.datetime.today().isoformat()[:10]

divisions = {
    "AL East": ["BOS", "NYY", "TBR", "TOR", "BAL"],
    "AL Central": ["CLE", "MIN", "KCR", "CHW", "DET"],
    "AL West": ["HOU", "LAA", "SEA", "TEX", "OAK"],
    "NL East": ["WSN", "MIA", "ATL", "NYM", "PHI"],
    "NL Central": ["CHC", "MIL", "STL", "PIT", "CIN"],
    "NL West": ["LAD", "ARI", "COL", "SDP", "SFG"],
}
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
team_colors = {
    "BOS": "#BD3039",
    "NYY": "#003087",
    "TBR": "#8FBCE6",
    "KCR": "#BD9B60",
    "CHW": "#27251F",
    "BAL": "#DF4601",
    "CLE": "#E31937",
    "MIN": "#002B5C",
    "DET": "#FA4616",
    "HOU": "#EB6E1F",
    "LAA": "#BA0021",
    "SEA": "#005C5C",
    "TEX": "#003278",
    "OAK": "#003831",
    "WSN": "#14225A",
    "MIA": "#FF6600",
    "ATL": "#13274F",
    "NYM": "#002D72",
    "PHI": "#E81828",
    "CHC": "#0E3386",
    "MIL": "#B6922E",
    "STL": "#C41E3A",
    "PIT": "#FDB827",
    "CIN": "#C6011F",
    "LAD": "#005A9C",
    "ARI": "#A71930",
    "COL": "#33006F",
    "SDP": "#002D62",
    "SFG": "#FD5A1E",
    "TOR": "#134A8E",
}
DB_TABLES = [
    "hits",
    "strikes",
    "balls",
    "lefty_st",
    "righty_st",
    "st_fastballs",
    "st_offspeed",
    "strikeouts",
]


def create_team_dfs(year: int, divisions: dict):
    """
    Creates a dictionary of pandas dataframes for each team's game logs.

    Args:
        year (int): The year for which game logs are fetched.
        divisions (dict): A dictionary where keys are division names and values are lists of team names.

    Returns:
        dict: A dictionary where keys are team names and values are pandas dataframes.
    """
    team_dfs = {
        team: pyb.team_game_logs(year, team)
        for teams in divisions.values() for team in teams
    }

    for df in team_dfs.values():
        df[["Rslt", "Score"]] = df["Rslt"].str.split(",", expand=True)

    return team_dfs


def preprocess_data(dataframes_dict: dict):
    """
    Preprocesses the data in the dictionary of dataframes.

    Args:
        dataframes_dict (dict): A dictionary where keys are table names and values are pandas dataframes.

    Returns:
        dict: The processed dataframes dictionary.
    """
    for df in dataframes_dict.values():
        # Fill NA/NaN values with 0
        df.fillna(0, inplace=True)

        # Convert string columns to lowercase for consistency
        for col in df.select_dtypes(include="object"):
            df[col] = df[col].str.lower()

    return dataframes_dict


def visualize_data(dataframes_dict: dict, team_colors: dict):
    """
    Visualizes the data in the dictionary of dataframes.

    Args:
        dataframes_dict (dict): A dictionary where keys are table names and values are pandas dataframes.
        team_colors (dict): A dictionary where keys are team names and values are color codes.
    """
    for team, df in dataframes_dict.items():
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=df, palette=team_colors[team])
        plt.title(f"{team} Data Visualization")
        plt.show()


def analyze_data(dataframes_dict: dict):
    """
    Performs statistical analysis on the data in the dictionary of dataframes.

    Args:
        dataframes_dict (dict): A dictionary where keys are table names and values are pandas dataframes.

    Returns:
        dict: The analysis results.
    """
    analysis_results = {}

    for team, df in dataframes_dict.items():
        analysis_results[team] = df.describe()

    return analysis_results


if __name__ == "__main__":
    dataframes_dict = pull_data_from_db(
        ".\\data\\statcast_events.db", DB_TABLES)
    team_dfs = create_team_dfs(2022, divisions)

    # Preprocess data
    processed_dfs = preprocess_data(dataframes_dict)
    processed_team_dfs = preprocess_data(team_dfs)

    # Visualize data
    visualize_data(processed_team_dfs, team_colors)

    # Analyze data
    analysis_results = analyze_data(processed_team_dfs)
    print(analysis_results)
    analysis_results = analyze_data(processed_team_dfs)
    print(analysis_results)
