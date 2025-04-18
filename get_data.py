from nba_api.stats.endpoints import leaguegamelog
import pickle


# d = leaguegamelog.LeagueGameLog(season="2024-25", league_id="00").get_dict()


# with open("temp.pkl", "wb") as file_handle:
    # pickle.dump(d, file_handle)

with open("temp.pkl", "rb") as file_handle:
    d = pickle.load(file_handle)

print(d.keys())
data = d.get('resultSets')[0]
print(type(data))
print(len(data))
print(data.keys())
print("headers:", data.get('headers'))
print("rowSet:", data.get('rowSet')[0])
