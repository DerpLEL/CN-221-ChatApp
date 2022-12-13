import socket
import pickle
import sqlite3

conn = sqlite3.connect("database.db")

cur = conn.execute("SELECT * from USER")

print(cur.fetchall())

conn.close()
