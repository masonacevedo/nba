"""
goal: predict the playoffs based on elos and season at the end of the

regular season

"""
import pickle
from nba_api.stats.endpoints import playoffpicture



import calculate_elos_general




def predictPlayoffs(season):
    file_name = season + "_playoff_standings.pkl"
    print()
    print()
    
    with open(file_name, "rb") as f:
        playoff_standings = pickle.load(f)

    elo_dict = calculate_elos_general.getEloDictAtEndOfRegSeason(season)

    series = getInitialSeries(playoff_standings)


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
    
    westSeries - []
    for high, low in zip(west_seeds[0:4], list(reversed(west_seeds))[0:4]):
        westSeries.append((high, low))

    return {"east:" eastSeries, "west": westSeries}

def predictWinners(seriesDict):
    pass

predictPlayoffs("2024-25")
