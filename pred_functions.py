import sqlite3
import pandas as pd

# Specify the correct path to the database file
db_path = 'betting/data/databases/2022_gamelogs.db'  # Adjusted path to the uploaded file

# Connect to the SQLite database
conn = sqlite3.connect(db_path)

# List all tables in the database
query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = pd.read_sql_query(query, conn)

# Display the tables
tables
