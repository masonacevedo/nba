import sqlite3
import pickle
from nba_api.stats.endpoints import playoffpicture


seasons = [str(i) + "-" + str(i+1)[2:] for i in range(2024, 2025)]

conn = sqlite3.connect("playoff_picture.db")

# with open("playoff_picture_schema.sql","r") as f:
    # cursor.executescript(f.read())

for season in seasons:
    file_name = season + "_playoff_standings.pkl"
    with open(file_name, "rb") as f:
        d = pickle.load(f)
    
    data = d.get('resultSets')[0]
    headers = data.get('headers')
    rows = data.get('rowSet')
    for header, datum in zip(headers, rows[0]):
        print(header,":",datum)

    breakpoint()


