import argparse

import requests

import pandas as pd

# Obtain the api key that was passed in from the command line
parser = argparse.ArgumentParser(description='Sample V4')
parser.add_argument('--api-key', type=str, default='')
args = parser.parse_args()


# An api key is emailed to you when you sign up to a plan
# Get a free API key at https://api.the-odds-api.com/
API_KEY = args.api_key or '1628e7b26fd53acf9eef611ac3466368'


# Sport key
# Alternatively use 'upcoming' to see the next 8 games across all sports
SPORT = 'baseball_mlb'

# Bookmaker regions
# uk | us | us2 | eu | au. Multiple can be specified if comma delimited.
REGIONS = 'us2'

# h2h | spreads | totals. Multiple can be specified if comma delimited
# Note only featured markets (h2h, spreads, totals) are available with the odds endpoint.
MARKETS = 'h2h'

# Odds format
# decimal | american
ODDS_FORMAT = 'american'

# Date format
# iso | unix
DATE_FORMAT = 'iso'

# Bookmaker
# hardrockbet
BOOKMAKER = 'hardrockbet'

#todays date as DATE
DATE = input("Enter date in YYYY-MM-DD format: ")


odds_response = requests.get(f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds', params={
    'api_key': API_KEY,
    'regions': REGIONS,
    'markets': MARKETS,
    'oddsFormat': ODDS_FORMAT,
    'dateFormat': DATE_FORMAT,
    'bookmakers' : BOOKMAKER,
    'date': DATE
})
global api_data
api_data = []

# Check if the request was successful
if odds_response.status_code != 200:
    print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')
    

else:
    odds_json = odds_response.json()
    api_data = odds_response.json()
  # Check the usage quota
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])
    
# Initialize a list to store your processed data
processed_data = []

# Loop through each event in the API data
for event in api_data:
    # Extract event details
    event_details = {
        'id': event['id'],
        'sport_title': event['sport_title'],
        'commence_time': event['commence_time'],
        'home_team': event['home_team'],
        'away_team': event['away_team'],
    }
    
    # Check if there are bookmakers for this event
    if event['bookmakers']:
        # Loop through each bookmaker in the event
        for bookmaker in event['bookmakers']:
            # Check if there are markets for this bookmaker
            if bookmaker['markets']:
                # Loop through each market for the bookmaker
                for market in bookmaker['markets']:
                    # Check if the market key is 'h2h' for head-to-head odds
                    if market['key'] == 'h2h':
                        # Loop through each outcome in the market to extract odds
                        for outcome in market['outcomes']:
                            # Prepare a dictionary with event, bookmaker, and odds details
                            data_row = {**event_details,
                                        'bookmaker': bookmaker['title'],
                                        'outcome_name': outcome['name'],
                                        'odds': outcome['price']}
                            # Append the dictionary to the processed data list
                            processed_data.append(data_row)
    else:
        # If no bookmakers, still append the event details with empty values for the rest
        processed_data.append({**event_details, 'bookmaker': None, 'outcome_name': None, 'odds': None})

# Create a DataFrame from the processed data
df = pd.DataFrame(processed_data)

# Display the DataFrame to verify its structure
df.to_csv(f'betting/data/odds/{DATE}_odds.csv', index=False)
print(df)


# First, let's drop rows where odds are NaN as these do not contain valid bookmaker odds
df = df.dropna(subset=['odds'])

def odds_to_probability(odds):
    if odds > 0:
        return 100 / (odds + 100)
    else:
        return -odds / (-odds + 100)

# Apply the conversion function to each odds value
df['probability'] = df['odds'].apply(odds_to_probability)

# Now, you might want to aggregate these probabilities by game ID
# For simplicity, let's calculate the average probability for each outcome within a game
# This is a basic approach; you may need a more sophisticated method depending on your model's needs

# Group by game ID and outcome_name, then calculate the mean probability
game_probabilities = df.groupby(['id', 'outcome_name'])['probability'].mean().reset_index()

# If you need a pivot table with teams on columns and probabilities as values
game_probabilities_pivot = game_probabilities.pivot(index='id', columns='outcome_name', values='probability').reset_index()

game_probabilities.to_csv(f'betting/data/probabilities/{DATE}_probabilities.csv', index=False)