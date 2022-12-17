import sqlite3

conn = sqlite3.connect("database.db")

conn.execute('UPDATE USER set ONLINE = -1 where USERNAME != "!";')
conn.commit()

'''
cur = conn.execute(f"""SELECT USERNAME, PORT FROM USER INNER JOIN (SELECT FR FROM FRIEND where USERNAME = "Bob") as t1 WHERE USERNAME = FR""").fetchall()
print(cur)
'''
conn.close()