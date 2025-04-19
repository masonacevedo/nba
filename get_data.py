from nba_api.stats.endpoints import leaguegamelog
import pickle
import sqlite3

def buildDict(headers, row):
    game = dict(zip(headers, row))
    game["SEASON_ID"] = int(game["SEASON_ID"])
    game["TEAM_ID"] = int(game["TEAM_ID"])
    game["GAME_ID"] = int(game["GAME_ID"])
    game["MIN"] = int(game["MIN"])
    game["FG_PCT"] = float(game["FG_PCT"])
    game["FG3_PCT"] = float(game["FG3_PCT"])
    game["FT_PCT"] = float(game["FT_PCT"])
    game["PLUS_MINUS"] = float(game["PLUS_MINUS"])
    game["VIDEO_AVAILABLE"] = bool(game["VIDEO_AVAILABLE"])    
    return game

# d = leaguegamelog.LeagueGameLog(season="2024-25", league_id="00").get_dict()


# with open("temp.pkl", "wb") as file_handle:
    # pickle.dump(d, file_handle)

with open("temp.pkl", "rb") as file_handle:
    d = pickle.load(file_handle)

data = d.get('resultSets')[0]

headers = data.get('headers')
rows = data.get('rowSet')

conn = sqlite3.connect("leaguegamelog.db")
cursor = conn.cursor()

with open("schema.sql", "r") as f:
    cursor.executescript(f.read())

print("successfully made table")

for index, row in enumerate(rows):
    game = buildDict(headers, row)
    cursor.execute(f"""
INSERT OR REPLACE INTO games (
    {', '.join(headers)}
) VALUES (
    {', '.join(':' + h for h in headers)}
)
""", game)

conn.commit()
conn.close()
