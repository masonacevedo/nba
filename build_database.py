import sqlite3
import pickle
from nba_api.stats.endpoints import playoffpicture


seasons = [str(i) + "-" + str(i+1)[2:] for i in range(1946, 2025)]

conn = sqlite3.connect("playoff_picture.db")
cursor = conn.cursor()
with open("playoff_picture_schema.sql","r") as f:
    cursor.executescript(f.read())

for season in seasons:
    file_name = season + "_playoff_standings.pkl"
    with open(file_name, "rb") as f:
        d = pickle.load(f)
    
    data = d.get('resultSets')[0]
    headers = data.get('headers')
    rows = data.get('rowSet')
    for row in rows:
        game = {header:item for item, header in zip(row, headers)}
        cursor.execute(f"""
            INSERT OR REPLACE INTO playoff_picture (
                {', '.join(headers)}
            ) VALUES (
                {', '.join(':' + h for h in headers)}
            )""", game)


# cursor.execute("SELECT * FROM playoff_picture")
# games = cursor.fetchall()
# for g in games:
    # print(g)
    input()
