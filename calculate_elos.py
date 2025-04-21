import read_games_from_dbs
import pickle
from nba_api.stats.static import teams
from nba_api.stats.static import teams

K_FACTOR = float(8)

def calcProbability(elo1, elo2):
    """returns the probability that the entity with the 1st elo will win a single game"""
    diff = elo2 - elo1
    exponent = float(diff)/float(400)
    return float(1)/(float(1)+10**exponent)

def indexOf(columns, var):
    return [col[1] for col in columns].index(var)



def print_translated(elo_dict):
    all_names = []
    for k in elo_dict.keys():
        if teams.find_team_name_by_id(k):
            all_names.append(teams.find_team_name_by_id(k).get("full_name"))
    # filter out the nones
    longest_name = max(len(name) for name in all_names)
    for k,v in sorted(elo_dict.items(), key = lambda i: i[1], reverse=True):
        if teams.find_team_name_by_id(k):
            name = teams.find_team_name_by_id(k).get("full_name")
            print(name, " " * (longest_name - len(name)),":", v)

def updateEloDict(columns, game, elo_dict, games_seen):
    # print_translated(elo_dict)
    SEASON_ID_INDEX = indexOf(columns, "SEASON_ID")
    season_id = game[SEASON_ID_INDEX]

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
    
    if "vs." in matchup:
        team_abs = [t.replace(" ","") for t in matchup.split("vs.")]
    elif "@" in matchup:
        team_abs = [t.replace(" ","") for t in matchup.split("@")]
    else:
        raise Exception("neither 'vs' nor '@' found in matchup")


    team_ids = [abs_to_ids.get((ab, season_id)) for ab in team_abs]

    prob1 = "1610610024"
    prob2 = "1610612752"
    prob3 = "1610612761"
    
    WL_INDEX = indexOf(columns, "WL")
    result = game[WL_INDEX]
    
    if result == "W":
        winner_id = team_id
        team_ids.remove(winner_id)
        loser_id = team_ids[0]
    elif result == "L":
        loser_id = team_id
        team_ids.remove(loser_id)
        winner_id = team_ids[0]
    else:
        if game == (22012, 1610612754, 'IND', 'Indiana Pacers', 21201214, '2013-04-16', 'IND @ BOS', None, 0.0, 0, 0, None, 0, 0, None, 0, 0, None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 'regular season'):
            """This game was cancelled due to the boston marathon, and never was actually played"""
            return

        raise Exception("result is neither 'W' nor 'L'")
    
    if winner_id not in elo_dict:
        elo_dict[winner_id] = 800
    if loser_id not in elo_dict:
        elo_dict[loser_id] = 800
    
    win_probability_of_winner = calcProbability(elo_dict[winner_id], elo_dict[loser_id])
    
    # print("old elos:")
    # print(elo_dict[winner_id], elo_dict[loser_id])
    elo_dict[winner_id] = elo_dict[winner_id] + (K_FACTOR*(1 - win_probability_of_winner))
    elo_dict[loser_id] = elo_dict[loser_id] - (K_FACTOR*(1-win_probability_of_winner))
    # print("new elos:")
    # print(elo_dict[winner_id], elo_dict[loser_id])
    # print()
   
    # print_translated(elo_dict)
    # input()
    

columns, games = read_games_from_dbs.getAllGames()
with open("abs_to_ids.pkl","rb") as f:
    abs_to_ids = pickle.load(f)


elo_dict = {}
games_seen = set()
for game in games:
    updateEloDict(columns, game, elo_dict, games_seen)
print_translated(elo_dict)
