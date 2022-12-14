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

    row = conn.execute(f"""SELECT * from USER where USERNAME = "{message['user']}";""").fetchone()

    if not row:
        conn.execute(f"""INSERT INTO USER(USERNAME, PASSWORD, PORT, ONLINE)
                         VALUES("{message["user"]}", "{message["password"]}", -1, -1);""")
        conn.commit()
        cSock.send("Affirm".encode())
        print(f"User {message['user']} has been registered.")
    else:
        cSock.send("Exist".encode())
        print(f"Failed to register new user.")

    conn.close()

def login(message, cSock):
    conn = sqlite3.connect("database.db")

    row = conn.execute(f"""SELECT * from USER where USERNAME = "{message['user']}";""").fetchone()

    if not row:
        cSock.send("Exist".encode())
        print(f"Account user {message['user']} in database.")

    elif row[1] != message["password"]:
        cSock.send("Incorrect".encode())
        print(f'Incorrect password for {message["user"]} entered.')

    elif row[3] == 1:
        cSock.send("Relog".encode())
        print(f'Already logged in user {message["user"]} attempting to log in again.')

    else:
        cSock.send("Affirm".encode())

        conn.execute(f"""UPDATE USER set PORT = {message["port"]} where USERNAME = "{message["user"]}";""")
        conn.execute(f"""UPDATE USER set ONLINE = 1 where USERNAME = "{message["user"]}";""")
        conn.commit()

        print(f'User {message["user"]} has logged in.')

    conn.close()

def logout(message, cSock):
    conn = sqlite3.connect("database.db")

    conn.execute(f"""UPDATE USER set PORT = -1 where USERNAME = "{message["user"]}";""")
    conn.execute(f"""UPDATE USER set ONLINE = -1 where USERNAME = "{message["user"]}";""")
    conn.commit()

    print(f"User {message['user']} has logged out.")
    conn.close()

def getpub(message, cSock):
    conn = sqlite3.connect("database.db")

    clnlist = list()

    if message['user'] == "ALL":
        cur = conn.execute("SELECT USERNAME, PORT from USER where ONLINE = 1").fetchall()

        for row in cur:
            clnlist.append((row[0], row[1]))

        msg = pickle.dumps(clnlist)
        msg = bytes(f"{len(msg):<10}", "utf-8") + msg
        cSock.send(msg)

    else:
        cur = conn.execute(f"""SELECT USERNAME, PORT from USER where ONLINE = 1 AND USERNAME = {message['user']}""").fetchall()

        if cur:
            for row in cur:
                clnlist.append((row[0], row[1]))

            msg = pickle.dumps(clnlist)
            msg = bytes(f"{len(msg):<10}", "utf-8") + msg
            cSock.send(msg)

    conn.close()


def addf(message, cSock):
    conn = sqlite3.connect("database.db")
    cur = conn.execute(f"""SELECT FR FROM FRIEND where USERNAME = "{message['user']}";""").fetchall()

    if not cur:
        conn.execute(f"""INSERT INTO FRIEND(USERNAME, FR)
                    VALUES("{message['user']}", "{message['friend']}");""")
        conn.commit()
        print(f'{message["user"]} has added friend {message["friend"]}')
    else:
        cur = conn.execute(f"""SELECT FR FROM FRIEND where USERNAME = "{message['user']}" and FR = "{message['friend']}";""").fetchall()

        if not cur:
            conn.execute(f"""INSERT INTO FRIEND(USERNAME, FR)
                                VALUES("{message['user']}", "{message['friend']}");""")
            conn.commit()
            print(f'{message["user"]} has added friend {message["friend"]}')
        else:
            print(f"{message['user']} already added {message['friend']}")

    conn.close()

def getf(message, cSock):
    conn = sqlite3.connect("database.db")

    clnlist = list()

    cur = conn.execute(f"""SELECT USERNAME, PORT FROM USER INNER JOIN (SELECT FR FROM FRIEND where USERNAME = "{message['user']}") as t1 WHERE USERNAME = FR and PORT != -1;""").fetchall()

    for row in cur:
        clnlist.append((row[0], row[1]))

    msg = pickle.dumps(clnlist)
    msg = bytes(f"{len(msg):<10}", "utf-8") + msg
    cSock.send(msg)

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
        t = Thread(target=login, args=(data, cSock,))
        t.start()

    elif data["type"] == "logout":
        t = Thread(target=logout, args=(data, cSock,))
        t.start()

    elif data["type"] == "addf":
        t = Thread(target=addf, args=(data, cSock,))
        t.start()

    elif data["type"] == "getpub":
        t = Thread(target=getpub, args=(data, cSock,))
        t.start()

    elif data["type"] == "getf":
        t = Thread(target=getf, args=(data, cSock,))
        t.start()