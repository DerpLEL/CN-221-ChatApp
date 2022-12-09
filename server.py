import socket
from threading import Thread
from datetime import datetime
import sys

namePass = {"admin": "12345"}

def processor(cSock):
    while True:
        msg = cSock.recv(1024).decode()
        print(f"msg")

s = socket.socket()

host = "0.0.0.0"
port = 5002

clients = set()

s.bind((host, port))

s.listen(5)

while True:
    cSock, cAddr = s.accept()
    print(f"Client {cAddr} has connected.")

    t = Thread(target=processor, args=(cSock,))
    t.daemon = True
    t.start()
