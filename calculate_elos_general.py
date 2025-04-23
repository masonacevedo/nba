import read_games_from_dbs
import pickle
import argparse


from nba_api.stats.static import teams
from nba_api.stats.static import teams

parser = argparse.ArgumentParser()
parser.add_argument('-k','--k-factor',
                    help="The K_FACTOR for ELO calculations. Default value is 8. Higher values mean more fast/sensitive adjustments, and vice versa.",
                    type=float)
parser.add_argument('-m', '--calc-method',
                    help=("n - normal: Each team gets an ELO rating that updates normally"
                          "d - distinct: Each team gets a distinct ELO rating for home agames and away games"
                          "v - variable: Each team gets a distcint ELO rating for home games and away games, but home wins/losses also contribute some amount to the away wins/losses (and vice versa), as determined by a 'Cross Factor', which must also be passed in, if using 'variable' calculation"),
                    choices=['n', 'd', 'v'],
                    )

parser.add_argument('-C', '--CROSS_FACTOR',
                    type=float)

args = parser.parse_args()

if args.k_factor:
    K_FACTOR = args.k_factor

K_FACTOR = float(8)

if args.calc_method:
    if args.calc_method == "v":
        print("got here")
        if args.CROSS_FACTOR:
            print("also here")
            CROSS_FACTOR = args.CROSS_FACTOR
        else:
            raise Exception("variable calculation method requires you to specify a cross factor")
    elif args.calc_method == "d":
        CROSS_FACTOR = 0
else:
    args.calc_method = "n"
    CROSS_FACTOR = 0


def calcProbability(elo1, elo2):
    """returns the probability that the entity with the 1st elo will win a single game"""
    diff = elo2 - elo1
    exponent = float(diff)/float(400)
    return float(1)/(float(1)+10**exponent)

def indexOf(columns, var):
    return [col[1] for col in columns].index(var)



def print_translated_distinct_home_away(elo_dict):
    all_names = []
    for k in elo_dict.keys():
        team_id = k[0]
        if teams.find_team_name_by_id(team_id):
            all_names.append(teams.find_team_name_by_id(team_id).get("full_name"))
    # filter out the nones
    longest_name = max(len(name) for name in all_names)
    for k,v in sorted(elo_dict.items(), key = lambda i: i[1], reverse=True):
        team_id, homeawaystatus = k
        if teams.find_team_name_by_id(team_id):
            name = teams.find_team_name_by_id(team_id).get("full_name")
            print(name, " " * (longest_name - len(name)),",", homeawaystatus, ":", v)

def print_translated_normal(elo_dict):
    all_names = []
    for k in elo_dict.keys():
        team_id = k
        if teams.find_team_name_by_id(team_id):
            all_names.append(teams.find_team_name_by_id(team_id).get("full_name"))
    # filter out the nones
    longest_name = max(len(name) for name in all_names)
    for k,v in sorted(elo_dict.items(), key = lambda i: i[1], reverse=True):
        team_id = k
        if teams.find_team_name_by_id(team_id):
            name = teams.find_team_name_by_id(team_id).get("full_name")
            print(name, " " * (longest_name - len(name)), ":", v)

def home_team_won(columns, game):
    MATCHUP_INDEX = indexOf(columns, "MATCHUP")
    matchup = game[MATCHUP_INDEX]
    WL_INDEX = indexOf(columns, "WL")
    result = game[WL_INDEX]

    if "vs." in matchup:
        home_team, away_team = matchup.split(" vs. ")
    elif "@" in matchup:
        away_team, home_team = matchup.split(" @ ")

    TEAM_ABBREVIATION_INDEX = indexOf(columns, "TEAM_ABBREVIATION")

    team_abbreviation = game[TEAM_ABBREVIATION_INDEX]

    if team_abbreviation == home_team and result == "W":
        return True
    elif team_abbreviation == away_team and result == "W":
        return False
    elif team_abbreviation == home_team and result == "L":
        return False
    elif team_abbreviation == away_team and result == "L":
        return True
    else:
        raise Exception("Shoud be impossible to get here")

def updateElosNormal(elo_dict, winner_id, loser_id, K_FACTOR):
    if winner_id not in elo_dict:
        elo_dict[winner_id] = 800
    if loser_id not in elo_dict:
        elo_dict[loser_id] = 800
    win_probability_of_winner = calcProbability(elo_dict[winner_id], elo_dict[loser_id])
    elo_dict[winner_id] = elo_dict[winner_id] + (K_FACTOR*(1 - win_probability_of_winner))
    elo_dict[loser_id] = elo_dict[loser_id] - (K_FACTOR*(1-win_probability_of_winner))


def updateElosVariable(game, columns, elo_dict, winner_id, loser_id, K_FACTOR, CROSS_FACTOR):
    if (winner_id, "home") not in elo_dict:
        elo_dict[(winner_id, "home")] = 800
    if (winner_id, "away") not in elo_dict:
        elo_dict[(winner_id, "away")] = 800
 
    if (loser_id, "home") not in elo_dict:
        elo_dict[(loser_id, "home")] = 800
    if (loser_id, "away") not in elo_dict:
        elo_dict[(loser_id, "away")] = 800
 
    if home_team_won(columns, game): 
        win_probability_of_winner = calcProbability(elo_dict[(winner_id, "home")], elo_dict[loser_id, "away"])
        elo_dict[(winner_id, "home")] = elo_dict[(winner_id, "home")] + (K_FACTOR*(1 - win_probability_of_winner))
        elo_dict[(loser_id, "away")] = elo_dict[(loser_id, "away")] - (K_FACTOR*(1-win_probability_of_winner))
 
        elo_dict[(winner_id, "away")] = elo_dict[(winner_id, "away")] + CROSS_FACTOR * (K_FACTOR*(1 - win_probability_of_winner))
        elo_dict[(loser_id, "home")] = elo_dict[(loser_id, "home")] - CROSS_FACTOR * (K_FACTOR*(1-win_probability_of_winner))
    elif not(home_team_won(columns, game)):
        win_probability_of_winner = calcProbability(elo_dict[(winner_id, "away")], elo_dict[loser_id, "home"])
        elo_dict[(winner_id, "away")] = elo_dict[(winner_id, "away")] + (K_FACTOR*(1 - win_probability_of_winner))
        elo_dict[(loser_id, "home")] = elo_dict[(loser_id, "home")] - (K_FACTOR*(1-win_probability_of_winner))
 
        elo_dict[(winner_id, "home")] = elo_dict[(winner_id, "home")] + CROSS_FACTOR * (K_FACTOR*(1 - win_probability_of_winner))
        elo_dict[(loser_id, "away")] = elo_dict[(loser_id, "away")] - CROSS_FACTOR * (K_FACTOR*(1-win_probability_of_winner))
    else:
        raise Exception("neither home team nor away team won!")


def getWinnerAndLoser(team_id, team_ids, result):
    if result == "W":
        winner_id = team_id
        just_ids = [team_id[0] for team_id in team_ids]
        just_ids.remove(winner_id)
        loser_id = just_ids[0]
    elif result == "L":
        loser_id = team_id
        just_ids = [team_id[0] for team_id in team_ids]
        just_ids.remove(loser_id)
        winner_id = just_ids[0]
    else:
        raise Exception("result is neither 'W' nor 'L'")
    return winner_id, loser_id
    
def getTeamAbbreviations(matchup):
    if "vs." in matchup:
        team_abbreviations = [t.replace(" ","") for t in matchup.split("vs.")]
        team_abbreviations[0] = (team_abbreviations[0], "home")
        team_abbreviations[1] = (team_abbreviations[1], "away")
    elif "@" in matchup:
        team_abbreviations = [t.replace(" ","") for t in matchup.split("@")]
        team_abbreviations[0] = (team_abbreviations[0], "away")
        team_abbreviations[1] = (team_abbreviations[1], "home")
    else:
        raise Exception("neither 'vs' nor '@' found in matchup")
    return team_abbreviations

def updateEloDict(columns, game, elo_dict, games_seen, abs_to_ids, CROSS_FACTOR=0):
    if game in [(22012, 1610612754, 'IND', 'Indiana Pacers', 21201214, '2013-04-16', 'IND @ BOS', None, 0.0, 0, 0, None, 0, 0, None, 0, 0, None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 'regular season'),
                (22012, 1610612738, 'BOS', 'Boston Celtics', 21201214, '2013-04-16', 'BOS vs. IND', None, 0.0, 0, 0, None, 0, 0, None, 0, 0, None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0, 'regular season')]:
        """This game was cancelled due to the boston marathon bombing, and never was actually played"""
        return
    print("game:", game)

    GAME_ID_INDEX = indexOf(columns, "GAME_ID")
    game_id = game[GAME_ID_INDEX]

    # games often appear twice. *shrug*
    if game_id in games_seen:
        return
    games_seen.add(game_id)

    SEASON_ID_INDEX = indexOf(columns, "SEASON_ID")
    season_id = game[SEASON_ID_INDEX]
    
    TEAM_ID_INDEX = indexOf(columns,"TEAM_ID")
    team_id = game[TEAM_ID_INDEX]
    
    MATCHUP_INDEX = indexOf(columns, "MATCHUP")
    matchup = game[MATCHUP_INDEX]

    team_abbreviations = getTeamAbbreviations(matchup)
    team_ids = [(abs_to_ids.get((ab[0], season_id)), ab[1]) for ab in team_abbreviations]
    
    WL_INDEX = indexOf(columns, "WL")
    result = game[WL_INDEX]
    winner_id, loser_id = getWinnerAndLoser(team_id, team_ids, result)
    
    if args.calc_method == "n":
        updateElosNormal(elo_dict, winner_id, loser_id, K_FACTOR)
    elif args.calc_method == "v":
        updateElosVariable(game, columns, elo_dict, winner_id, loser_id, K_FACTOR, CROSS_FACTOR)
    elif args.calc_method == "d":
        updateElosVariable(game, columns, elo_dict, winner_id, loser_id, K_FACTOR, CROSS_FACTOR=0)
    else:
        raise Exception("invalid calculation method, should impossible to get here")


def getEloDictAtEndOfRegSeason(season):
    columns, games = read_games_from_dbs.getAllGames()
    with open("abs_to_ids.pkl","rb") as f:
        abs_to_ids = pickle.load(f)
    
    elo_dict = {}
    games_seen = set()
    
    for index, game in enumerate(games):
        playoffSeasonID = "4" + season[0:4]
        if str(game[0]) == playoffSeasonID:
            break
        updateEloDict(columns, game, elo_dict, games_seen, abs_to_ids, CROSS_FACTOR)
    
    if args.calc_method == "n":
        print_translated_normal(elo_dict)
    elif args.calc_method == "v" or args.calc_method == "d":
        print_translated_distinct_home_away(elo_dict)

getEloDictAtEndOfRegSeason("2016-17")
