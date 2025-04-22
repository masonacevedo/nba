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

x_vals = list(np.linspace(0,1,401))
y_vals = [sevenGameSeriesProb(p) for p in x_vals]
z_vals = [probabilityManySeries(p, 1000) for p in x_vals]

for x, y in zip(x_vals, y_vals):
    print(float(x), ":", float(y), ":",predictMatchup(x))

plt.plot(x_vals, y_vals, ".")
plt.plot(x_vals, z_vals, ".")
plt.show()
