from nba_api.stats.endpoints import leaguegamelog, leaguegamefinder

# d = leaguegamelog.LeagueGameLog(season="2024-25", date_from_nullable="2025-04-14", date_to_nullable="2025-04-19", season_type="").get_dict()

d = leaguegamefinder.LeagueGameFinder(season_nullable="2024-25").get_dict()

data = d.get('resultSets')[0]
headers = data.get('headers')
rows = data.get('rowSet')

playin_games = list(filter(lambda row: row[0][0] =="5", rows))
for row in playin_games:
    print(row)
