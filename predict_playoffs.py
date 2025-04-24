"""
goal: predict the playoffs based on elos and season at the end of the

regular season

"""
import pickle
from nba_api.stats.endpoints import playoffpicture



import calculate_elos_general
import probability



def predictPlayoffs(season):
    file_name = season + "_playoff_standings.pkl"
    print()
    print()
    
    with open(file_name, "rb") as f:
        playoff_standings = pickle.load(f)

    elo_dict = calculate_elos_general.getEloDictAtEndOfRegSeason(season)

    series = getInitialSeries(playoff_standings)
    predictWinners(playoff_standings, series, elo_dict)

def easternSeed(row, seedNum, headers):
    conference_index = headers.index("Conference")
    seed_index = headers.index('PlayoffSeeding')
    return row[conference_index] == "East" and row[seed_index] == seedNum

def westernSeed(row, seedNum, headers):
    conference_index = headers.index("Conference")
    seed_index = headers.index('PlayoffSeeding')
    return row[conference_index] == "West" and row[seed_index] == seedNum

def getEastSeed(rows, n, headers):
    return list(filter(lambda row: easternSeed(row, n, headers), rows))[0]

def getWestSeed(rows, n, headers):
    return list(filter(lambda row: westernSeed(row, n, headers), rows))[0]

def getInitialSeries(playoff_standings):
    resultSets = playoff_standings.get('resultSets')[0]
    headers = resultSets.get('headers')
    rows = resultSets.get('rowSet')

    for row in rows:
        seed_index = headers.index("PlayoffSeeding")
        team_index = headers.index("TeamName")
   
    east_seeds = [getEastSeed(rows, n, headers) for n in range(1,9)] 
    west_seeds = [getWestSeed(rows, n, headers) for n in range(1,9)] 
    
    eastSeries = []
    
    for high, low in zip(east_seeds[0:4], list(reversed(east_seeds))[0:4]):
        eastSeries.append((high, low))
    
    westSeries = []
    for high, low in zip(west_seeds[0:4], list(reversed(west_seeds))[0:4]):
        westSeries.append((high, low))

    return {"east": eastSeries, "west": westSeries}


def win_prob_from_outcomes(outcomes):
    win_outcomes = filter(lambda k: "win" in k, outcomes.keys())
    return sum([outcomes[x] for x in win_outcomes])

def predictWinners(playoff_standings, seriesDict, elo_dict):
    resultSets = playoff_standings.get('resultSets')[0]
    headers = resultSets.get('headers')
    team_id_index = headers.index("TeamID")
    team_index = headers.index("TeamName")
    
    eastSeries = seriesDict.get("east")
    westSeries = seriesDict.get("west")
    

    for high_seed, low_seed in eastSeries + westSeries:
        high_seed_team_id = high_seed[team_id_index]
        low_seed_team_id = low_seed[team_id_index]
        outcomes = probability.predictSeriesFromElos(elo_dict[high_seed_team_id], elo_dict[low_seed_team_id])
        win_prob = win_prob_from_outcomes(outcomes)


        print(high_seed[team_index], ":", elo_dict[high_seed_team_id])
        print(low_seed[team_index], ":", elo_dict[low_seed_team_id])
        for k,v in outcomes.items():
            print(k,":",v)


        s1 = "P(" + high_seed[team_index] + " win):"
        s2 = "P(" + low_seed[team_index] + " win):"
        

        l = max(len(s1),len(s2))

        prettyS1 = s1 + " "*(l - len(s1))
        prettyS2 = s2 + " "*(l - len(s2))   
        # print("len(prettyS1):",len(prettyS1))
        # print("len(prettyS2):",len(prettyS2))
        print(prettyS1, win_prob)
        print(prettyS2, 1 - win_prob)
        print("\n")


predictPlayoffs("2024-25")
