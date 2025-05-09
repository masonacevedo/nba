import math
import numpy as np
import matplotlib.pyplot as plt
import random

def sevenGameSeriesProb(p):
    q = 1 - p
    win_4 = p**4
    
    win_5 = ((p**4)*(q)*math.comb(5,1)) * (4/5)
    
    win_6 = ((p**4)*(q**2)*math.comb(6,2)) * (4/6)

    win_7 = ((p**4)*(q**3)*math.comb(7,3)) * (4/7)

    return sum((win_4, win_5, win_6, win_7))

def predictMatchup(p):
    q = 1 - p
    win_4 = ("win_4", p**4)
    win_5 = ("win_5", ((p**4)*(q)*math.comb(5,1)) * (4/5))
    win_6 = ("win_6", ((p**4)*(q**2)*math.comb(6,2)) * (4/6))
    win_7 = ("win_7", ((p**4)*(q**3)*math.comb(7,3)) * (4/7))

    lose_4 = ("lose_4", q**4)
    lose_5 = ("lose_5", ((q**4)*(p)*math.comb(5,1)) * (4/5))
    lose_6 = ("lose_6", ((q**4)*(p**2)*math.comb(6,2)) * (4/6))
    lose_7 = ("lose_7", ((q**4)*(p**3)*math.comb(7,3)) * (4/7))

    possible_results = [win_4, win_5, win_6, win_7, lose_4, lose_5, lose_6, lose_7]

    return max(possible_results, key=lambda result: result[1])[0]
    # return [(r[0], float(r[1])) for r in possible_results]

def simulateOneGame(p):
    return 1 if random.random() < p else 0

def simulateOneSeries(p):
    wins = 0
    losses = 0
    while (wins < 4) and (losses < 4):
        if simulateOneGame(p):
            wins += 1
        else:
            losses += 1
    
    if wins > losses:
        win_or_loss = "win"
    elif losses > wins:
        win_or_loss = "lose"
    else:
        raise Exception("Should be impossible to get here")

    return win_or_loss + "_" + str(wins+losses)

def most_common_item(lst):
    return max(set(lst), key=lst.count) 


def simulateManySeries(p, n = 100):
    results = [simulateOneSeries(p) for _ in range(0,n)]
    return most_common_item(results)

def probabilityManySeries(p, n=100):
    results = [simulateOneSeries(p) for _ in range(0,n)]
    wins = len(list(filter(lambda r: "win" in r, results)))
    return float(wins)/float(n)

def probabilityOfParticularSeries(seriesType, seriesOutcome, p_home, p_away):
    ans = 1
    for home_away_status, WL in zip(seriesType, seriesOutcome):
        if home_away_status == "H" and WL == "W":
            ans *= (p_home)
        elif home_away_status == "H" and WL == "L":
            ans *= (1-p_home)
        elif home_away_status == "A" and WL == "W":
            ans *= (p_away)
        elif home_away_status == "A" and WL == "L":
            ans *= (1-p_away)
        else:
            raise Exception("should be impossible to get here!")
    return ans


def validSeries(s):
    if len(s) > 7:
        return False
    if len(s) < 4:
        return False
    if s.count("W") > 4:
        return False
    if s.count("L") > 4:
        return False

    if s[-1] == "W" and s.count("W") < 4:
        return False
    if s[-1] == "L" and s.count("L") < 4:
        return False

    return True

def enumeratePossibilitiesRecursive(n):
    if n == 1:
        return ["W","L"]
    else:
        lowerResults = enumeratePossibilitiesRecursive(n-1)
        ans = []
        for r in lowerResults:
            ans.append("L"+r)
            ans.append("W"+r)
        return ans 

def enumeratePossibilities(n):
    preliminaryAnswers = enumeratePossibilitiesRecursive(n)
    return list(filter(validSeries, preliminaryAnswers))

def calculateSeriesWithHomeCourt(numGames, p_home, p_away, win_or_loss, seriesType = "HHAAHAH"):
    """numGames specifies how many games the series will go (i.e. 4-7)
        seriesType specifies 2-3-2 vs. 2-2-1-1-1 or wtv else
        outputs: The probability that the higher seed will win the series in numGames
    """
    WLPossibilities = enumeratePossibilities(numGames)
    correctOutcomes = filter(lambda s: s.count(win_or_loss) == 4, WLPossibilities)
    ans = 0 
    for possibility in correctOutcomes:
        ans += probabilityOfParticularSeries(seriesType, possibility, p_home, p_away)
    return ans

def predictSeriesFromProbalities(p_home, p_away):

    lose_4 = calculateSeriesWithHomeCourt(4, p_home, p_away, "L")
    lose_5 = calculateSeriesWithHomeCourt(5, p_home, p_away, "L")
    lose_6 = calculateSeriesWithHomeCourt(6, p_home, p_away, "L")
    lose_7 = calculateSeriesWithHomeCourt(7, p_home, p_away, "L")

    win_4 = calculateSeriesWithHomeCourt(4, p_home, p_away, "W")
    win_5 = calculateSeriesWithHomeCourt(5, p_home, p_away, "W")
    win_6 = calculateSeriesWithHomeCourt(6, p_home, p_away, "W")
    win_7 = calculateSeriesWithHomeCourt(7, p_home, p_away, "W")

    return {
        "lose_4": lose_4,
        "lose_5": lose_5,
        "lose_6": lose_6,
        "lose_7": lose_7,
        "win_4": win_4,
        "win_5": win_5,
        "win_6": win_6,
        "win_7": win_7,
    }


def elosToWinProb(elo1, elo2):
    """returns the probability that the entity with the 1st elo will win a single game"""
    diff = elo2 - elo1
    exponent = float(diff)/float(400)
    return float(1)/(float(1)+10**exponent)

def predictSeriesFromElos(high_seed_elo, low_seed_elo):
    probHighSeedWins = elosToWinProb(high_seed_elo, low_seed_elo)
    return predictSeriesFromProbalities(probHighSeedWins, probHighSeedWins)

def predictSeriesFromElosHomeCourt(high_seed_home_elo, high_seed_away_elo, low_seed_home_elo, low_seed_away_elo):
    probHighSeedWinsHome = elosToWinProb(high_seed_home_elo, low_seed_away_elo)
    probHighSeedWinsAway = elosToWinProb(high_seed_away_elo, low_seed_home_elo)
    return predictSeriesFromProbalities(probHighSeedWinsHome, probHighSeedWinsAway)
