from nba_api.stats.endpoints import leaguegamelog, leaguegamefinder
import pickle
import sqlite3
import time

def buildDict(headers, row):
    game = dict(zip(headers, row))
    game["SEASON_ID"] = int(game["SEASON_ID"]) if game["SEASON_ID"] is not None else None
    game["TEAM_ID"] = int(game["TEAM_ID"]) if game["TEAM_ID"] is not None else None
    game["GAME_ID"] = int(game["GAME_ID"]) if game["GAME_ID"] is not None else None
    game["MIN"] = int(game["MIN"]) if game["MIN"] is not None else None
    game["FG_PCT"] = float(game["FG_PCT"]) if game["FG_PCT"] is not None else None
    game["FG3_PCT"] = float(game["FG3_PCT"]) if game["FG3_PCT"] is not None else None
    game["FT_PCT"] = float(game["FT_PCT"]) if game["FT_PCT"] is not None else None
    game["PLUS_MINUS"] = float(game["PLUS_MINUS"]) if game["PLUS_MINUS"] is not None else None
    game["VIDEO_AVAILABLE"] = bool(game["VIDEO_AVAILABLE"])     if game["VIDEO_AVAILABLE"] is not None else None
    return game

conn = sqlite3.connect("leaguegamelog.db")
cursor = conn.cursor()
with open("schema.sql", "r") as f:
    cursor.executescript(f.read())
print("successfully made table")



seasons = [str(i) + "-" + str(i+1)[2:] for i in range(2024, 2025)]


for season in seasons:
    d = leaguegamelog.LeagueGameLog(season=season, league_id="00").get_dict()
    d_2 = leaguegamefinder.LeagueGameFinder(season_nullable=season, league_id_nullable="00").get_dict()
    data = d.get('resultSets')[0]
    data_2 = d_2.get('resultSets')[0]

    
    headers = data.get('headers')
    headers_2 = data_2.get('headers')
    print("headers:", headers)
    print("headers_2:", headers_2)
    input()

    rows = data.get('rowSet')
    rows2 = data_2.get('rowSet')
    print(f"there are {len(rows)} rows in the rowSet")
    
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
    print("data saved for season", season)
    time.sleep(30)
conn.close()
