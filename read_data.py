import sqlite3

with sqlite3.connect("leaguegamelog.db") as conn:
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(games)")
    columns = cursor.fetchall()


    cursor.execute("SELECT COUNT(*) FROM games")
    num_games = cursor.fetchone()[0]



    cursor.execute("SELECT * FROM games")

for col in columns:
    print(col)
print()
print(f"there are {num_games} games in the table")
for row in cursor:
    print(row)
    input()
