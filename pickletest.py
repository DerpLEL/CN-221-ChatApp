import sqlite3

conn = sqlite3.connect("database.db")

conn.execute(f'UPDATE USER set ONLINE = -1 WHERE USERNAME != "!";')
conn.commit()


conn.close()