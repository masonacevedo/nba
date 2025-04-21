from nba_api.stats.endpoints import franchisehistory, teamdetails
import sqlite3
import pickle
import time

with sqlite3.connect("leaguegamelog.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games")
ans = {}
for index, row in enumerate(cursor):
    
    season = row[0]
    team_id = row[1]
    # for some godforsaken reason, some team abbreviations just have a spacei n them. seems like there's no good reason for this.
    team_ab = row[2].replace(" ","")
    # print(ans)
    ans[(team_ab, season)] = team_id


with sqlite3.connect("leaguegamelog_playoffs.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games")

for row in cursor:
    season = row[0]
    team_id = row[1]
    team_ab = row[2]
        
    # print(ans)
    ans[(team_ab, season)] = team_id

with open("abs_to_ids.pkl", "wb") as f:
    pickle.dump(ans, f)

