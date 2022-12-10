import socket
import sqlite3
from threading import Thread
import sys
import pickle

def getData(cSock):
    length_header = cSock.recv(10)
    data_length = int(length_header.decode("utf-8").strip())
    msg = cSock.recv(data_length)
    return pickle.loads(msg)

def register(message, cSock):
    conn = sqlite3.connect("database.db")

    cur = conn.execute(f"""SELECT * from USER where USERNAME = "{message['user']}";""")
    row = cur.fetchone()

    if row == None:
        conn.execute(f"""INSERT INTO USER(USERNAME, PASSWORD, PORT, ONLINE)
                         VALUES("{message["user"]}", "{message["password"]}", -1, -1);""")
        conn.commit()
        cSock.send("Affirm".encode())
        print(f"User {message['user']} has been registered.")
    else:
        cSock.send("Exist".encode())
        print(f"Failed to register new user.")

    conn.close()

s = socket.socket()

host = "0.0.0.0"
port = 15000

s.bind((host, port))

s.listen(5)

while True:
    cSock, cAddr = s.accept()

    data = getData(cSock)
    if data["type"] == "register":
        t = Thread(target=register, args=(data,cSock,))
        t.start()

    elif data["type"] == "login":
        print()
    elif data["type"] == "logout":
        print()
    elif data["type"] == "addf":
        print()
    elif data["type"] == "getpub":
        print()
