import read_games_from_dbs
import pickle
from nba_api.stats.static import teams



def indexOf(columns, var):
    return [col[1] for col in columns].index(var)



def updateEloDict(columns, game, elo_dict, games_seen):
    GAME_ID_INDEX = indexOf(columns, "GAME_ID")
    game_id = game[GAME_ID_INDEX]
    # games often appear twice. *shrug*
    if game_id in games_seen:
        return
    games_seen.add(game_id)
    
    TEAM_ID_INDEX = indexOf(columns,"TEAM_ID")
    team_id = game[TEAM_ID_INDEX]
    
    MATCHUP_INDEX = indexOf(columns, "MATCHUP")
    matchup = game[MATCHUP_INDEX]
    
    if "vs" in matchup:
        team_abs = [t.replace(" ","") for t in matchup.split("vs")]
    elif "@" in matchup:
        team_abs = [t.replace(" ","") for t in matchup.split("@")]
    else:
        raise Exception("neither 'vs' nor '@' found in matchup")

    team_ids = [abs_to_ids.get(ab) for ab in team_abs]

    WL_INDEX = indexOf(columns, "WL")
    result = game[WL_INDEX]

    if result == "W":
        winner = team_id
        team_ids.remove(winner)
        loser = team_ids[0]
    elif result == "L":
        loser = team_id
        team_ids.remove(loser)
        winner = team_ids[0]
    else:
        raise Exception("result is neither 'W' nor 'L'")
    
    winner_id = abs_to_ids.get(winner)
    loser_id = abs_to_ids.get(loser)
    


columns, games = read_games_from_dbs.getAllGames()
with open("abs_to_ids.pkl","rb") as f:
    abs_to_ids = pickle.load(f)

print(columns)
print(games[0])

elo_dict = {}
games_seen = set()
updateEloDict(columns, games[0], elo_dict, games_seen)
print(elo_dict)
