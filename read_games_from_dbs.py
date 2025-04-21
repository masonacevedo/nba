import sqlite3
from datetime import datetime

def dateFromGame(game):
    year, month, day = game[5].split("-")
    return datetime(year=int(year),month=int(month),day=int(day))

def getAllGames():
    with sqlite3.connect("leaguegamelog.db") as reg_season_conn:
        reg_season_cursor = reg_season_conn.cursor()
        reg_season_cursor.execute("PRAGMA table_info(games)")
        columns = reg_season_cursor.fetchall()

        reg_season_cursor.execute("SELECT COUNT(*) FROM games")
        num_reg_season_games = reg_season_cursor.fetchone()[0]



        reg_season_cursor.execute("SELECT * FROM games")

    with sqlite3.connect("leaguegamelog_playoffs.db") as playoff_conn:
        playoff_cursor = playoff_conn.cursor()

        playoff_cursor.execute("SELECT COUNT(*) FROM games")
        num_playoff_games = playoff_cursor.fetchone()[0]

        playoff_cursor.execute("SELECT * FROM games")


    reg_season_games = reg_season_cursor.fetchall()
    playoff_games = playoff_cursor.fetchall()
    reg_season_games = [g + ("regular season",) for g in reg_season_games]
    playoff_games = [g + ("playoffs",) for g in playoff_games]

    all_games = reg_season_games + playoff_games


    print("len(reg_season_games)", len(reg_season_games))
    print("len(playoff_games", len(playoff_games))
    print("len(all_games)", len(all_games))

    all_games = sorted(all_games, key=lambda game: dateFromGame(game))
    return columns, all_games
