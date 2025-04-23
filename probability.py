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


def resultSeriesWithHomeCourt(p_home, p_away):
    # note: HOME always refers to the higher seed's home, and AWAY always refers
    # to the higher seeds AWAY
    q_home = 1 - p_home
    q_away = 1 - p_away

    win_4 = (p_home**2)*(p_away**2)
    win_5 = 2*((p_home**3)*p_away*q_away) + 2*((p_home**2)*(p_away**2)*q_home)
    win_6 = 6*((p_home**2)*(p_away**2)*(q_home)*(q_away)) + 3*((p_away**3)*(p_home)*(q_home**2)) + ((p_home**3)*(p_away)*(q_away**2))


def calculateSeriesWithHomeCourt(numGames, p_home, p_away, seriesType = "HHAAHAH"):
    """numGames specifies how many games the series will go (i.e. 4-7)
        seriesType specifies 2-3-2 vs. 2-2-1-1-1 or wtv else
        outputs: The probability that the higher seed will win the series in numGames
    """
    WLPossibilities = enumeratePossibilities(numGames)
    ans = 0 
    for possibility in WLPossibilities:
        ans += probabilityOfParticularSeries(seriesType, possibility, p_home, p_away)
    return ans
        


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

def enumeratePossibilities(n):
    preliminaryAnswers = enumeratePossibilitiesRecursive(n)
    return list(filter(validSeries, preliminaryAnswers))

def validSeries(s):
    if s[-1] == "L":
        return False
    if s.count("W") != 4:
        return False
    if s.count("L") > 3:
        return False
    return True

def enumeratePossibilitiesRecursive(n):
    if n == 1:
        return ["W"]
    else:
        lowerResults = enumeratePossibilitiesRecursive(n-1)
        ans = []
        for r in lowerResults:
            ans.append("L"+r)
            ans.append("W"+r)
        return ans 

def predictSeries(p_home, p_away):
    win_4 = calculateSeriesWithHomeCourt(4, p_home, p_away)
    win_5 = calculateSeriesWithHomeCourt(5, p_home, p_away)
    win_6 = calculateSeriesWithHomeCourt(6, p_home, p_away)
    win_7 = calculateSeriesWithHomeCourt(7, p_home, p_away)
    
    return sum((win_4,win_5,win_6,win_7))


num_points = 1000
away_win_probs = list(np.linspace(0.00,0.9,num_points))
home_win_probs = [p + 0.1 for p in away_win_probs]

home_court_vals = [predictSeries(p_home,p_away) for p_home,p_away in zip(home_win_probs, away_win_probs)]
standard_vals = [sevenGameSeriesProb(p_away) for p_away in away_win_probs]
plt.plot(away_win_probs, home_court_vals, ".")
plt.plot(away_win_probs, standard_vals, ".")
plt.plot(1000*[0.5], home_court_vals)
plt.plot(away_win_probs, 1000*[0.5])
plt.show()
