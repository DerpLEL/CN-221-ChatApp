#Rebuild everything using PyQt5
import socket
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from login import Ui_Frame as loginFrame
from mainInterface import Ui_MainWindow
from altChat import Ui_Frame as chatFrame
from register import Ui_Frame as regFrame
from threading import Thread
import pickle

currport = 5001
currusr = ""

connected = []

clnHost = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clnHost.bind(("127.0.0.1", currport))


def getData(sock):
    length_header = sock.recv(10)
    data_length = int(length_header.decode("utf-8").strip())
    msg = sock.recv(data_length)
    return pickle.loads(msg)


class registerWindow(QtWidgets.QMainWindow, regFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Register")
        self.usr = ""
        self.p1 = ""
        self.p2 = ""

        self.pushButton.clicked.connect(self.regchecksend)

        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.lineEdit_3.setEchoMode(QLineEdit.Password)

        self.lineEdit.editingFinished.connect(self.getusrname)
        self.lineEdit_2.editingFinished.connect(self.getp1)
        self.lineEdit_3.editingFinished.connect(self.getp2)

    def regchecksend(self):
        if self.usr == "" or self.p1 == "" or self.p2 == "" or self.p1 != self.p2:
            mg = QMessageBox.critical(self, "Error", "All fields are required and the passwords entered must match.")
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect(("127.0.0.1", 15000))
            except Exception:
                mg = QMessageBox.critical(self, "Error", "Can't connect to server, please try again later.")
                return

            message = dict()
            message["type"] = "register"
            message["user"] = self.usr
            message["password"] = self.p1

            msg = pickle.dumps(message)
            msg = bytes(f"{len(msg):<10}", "utf-8") + msg
            s.send(msg)

            rep = s.recv(1024).decode()
            if rep == "Affirm":
                mg = QMessageBox.information(self, "Success", "Registration successful, please login.")
                self.close()
            else:
                mg = QMessageBox.critical(self, "Error", "Account already exists, please pick another username or login.")

            s.close()

    def getusrname(self):
        self.usr = self.lineEdit.text()

    def getp1(self):
        self.p1 = self.lineEdit_2.text()

    def getp2(self):
        self.p2 = self.lineEdit_3.text()


class window(QtWidgets.QMainWindow, loginFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.usr = ""
        self.passw = ""
        self.setupUi(self)
        self.setWindowTitle("Login")

        self.pushButton_2.clicked.connect(self.loginmain)
        self.pushButton.clicked.connect(self.openreg)

        self.lineEdit_2.setEchoMode(QLineEdit.Password)

        self.lineEdit.editingFinished.connect(self.setusrname)
        self.lineEdit_2.editingFinished.connect(self.setpass)

    def loginmain(self):
        if self.usr == "" or self.passw == "":
            mg = QMessageBox.critical(self, "Error", "All fields are required.")
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect(("127.0.0.1", 15000))
            except Exception:
                mg = QMessageBox.critical(self, "Error", "Can't connect to server, please try again later.")
                return

            message = dict()
            message["type"] = "login"
            message["user"] = self.usr
            message["password"] = self.passw
            message["port"] = currport

            msg = pickle.dumps(message)
            msg = bytes(f"{len(msg):<10}", "utf-8") + msg
            s.send(msg)

            rep = s.recv(1024).decode()
            if rep == "Affirm":
                mg = QMessageBox.information(self, "Success", "Login success.")
                global currusr
                currusr = self.usr

                self.mainmenu = MainWin()
                self.mainmenu.show()
                self.close()

            elif rep == "Exist":
                mg = QMessageBox.critical(self, "Error", "Account does not exist, please register.")
            elif rep == "Relog":
                mg = QMessageBox.critical(self, "Error", "Account already logged in. Please log out before logging in again.")
            else:
                mg = QMessageBox.critical(self, "Error", "Incorrect password.")

            s.close()

    def openreg(self):
        self.regWin = registerWindow()
        self.regWin.show()

    def setusrname(self):
        self.usr = self.lineEdit.text()

    def setpass(self):
        self.passw = self.lineEdit_2.text()


class MainWin(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.clnlist = list()
        self.clnlist2 = list()
        self.setWindowTitle(f"Logged in as {currusr}")

        self.listWidget.itemActivated.connect(self.doubleclicked)
        self.listWidget_2.itemActivated.connect(self.doubleclicked)
        self.actionExit.triggered.connect(self.logout)

        self.updT = updateThread(self)
        self.updT.updateSignal.connect(self.updatelist)
        self.updT.start()

        self.listenner = connListener(self)
        self.listenner.updateSignal.connect(self.connRecv)
        self.listenner.start()

        self.updTFR = updateThreadFR(self)
        self.updTFR.updateSignal.connect(self.updatelistFR)
        self.updTFR.start()

    def doubleclicked(self, item):
        target = [x for x in self.clnlist if x[0] == item.data(1)]
        targetPort = target[0][1]

        if item.data(1) in connected:
            msg = QMessageBox.critical(None, "Error", "You are already connected to this user.")
            return

        print(f"Connecting to 127.0.0.1:{targetPort}")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(("127.0.0.1", targetPort))
        except Exception:
            mg = QMessageBox.critical(self, "Error", "Can't connect to user, user may have gone offline.")
            return

        print("Opening chat window...")
        s.sendall(currusr.encode())
        connected.append(item.data(1))

        self.newChat = chatWin(None, s, item.data(1))
        self.newChat.show()

    def connRecv(self, cSock):
        name = cSock.recv(1024).decode()
        connected.append(name)

        self.chatWindow = chatWin(None, cSock, name)
        self.chatWindow.show()

    def updatelist(self, items):
        items = [x for x in items if x[0] != currusr]
        self.clnlist = items
        self.listWidget.clear()

        for item in self.clnlist:
            listItem = QListWidgetItem(item[0])
            listItem.setData(1, item[0])
            self.listWidget.addItem(listItem)

    def updatelistFR(self, items):
        self.clnlist2 = items
        self.listWidget_2.clear()

        for item in self.clnlist2:
            listItem = QListWidgetItem(item[0])
            listItem.setData(1, item[0])
            self.listWidget_2.addItem(listItem)

    def logout(self):
        message = dict()
        message['type'] = 'logout'
        message['user'] = currusr

        msg = pickle.dumps(message)
        msg = bytes(f"{len(msg):<10}", "utf-8") + msg

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 15000))
        s.send(msg)

        s.close()
        mg = QMessageBox.information(self, "Logout", "Successfully logged out.")

        self.updT.stop()
        self.updTFR.stop()
        self.listenner.stop()
        self.close()

    def closeEvent(self, event):
        self.logout()

class chatWin(QtWidgets.QMainWindow, chatFrame):
    def __init__(self, parent=None, s=None, name=""):
        super().__init__(parent)
        self.setupUi(self)
        print(f"Connected username: {name}")

        self.label.setText(f"TALKING TO: {name}, AS {currusr}")
        self.peer = name
        self.targetSock = s
        self.msg = ""
        self.active = True

        self.lineEdit.returnPressed.connect(self.sendMsg)
        self.pushButton.clicked.connect(self.addfriend)

        t = Thread(target=self.listenmsg)
        t.start()

    def listenmsg(self):
        while self.active:
            try:
                msg = self.targetSock.recv(1024).decode()
            except Exception:
                self.updateText("The other user terminated the connection, you may close this window.")
                break

            msg = f">> {self.peer}: " + msg
            self.updateText(msg)

    def updateText(self, txt):
        self.textBrowser.append(txt)

    def addfriend(self):
        s = socket.socket()
        try:
            s.connect(("127.0.0.1", 15000))
        except Exception:
            mg = QMessageBox.critical(self, "Error", "Can't connect to server, please try again later.")
            return

        message = dict()
        message['type'] = "addf"
        message['user'] = currusr
        message['friend'] = self.peer

        msg = pickle.dumps(message)
        msg = bytes(f"{len(msg):<10}", "utf-8") + msg
        s.send(msg)

        s.close()

    def sendMsg(self):
        self.setmsg()
        self.lineEdit.clear()
        to_chat = "You: " + self.msg
        self.updateText(to_chat)

        try:
            self.targetSock.sendall(self.msg.encode())
        except Exception:
            pass

    def setmsg(self):
        self.msg = self.lineEdit.text()

    def closesession(self):
        self.targetSock.close()
        connected.remove(self.peer)

    def closeEvent(self, event):
        self.closesession()

class updateThread(QtCore.QThread):
    updateSignal = QtCore.pyqtSignal(list)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.active = True

    def run(self):
        while self.active:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect(("127.0.0.1", 15000))
            except Exception:
                self.updateSignal.emit([])
                continue

            message = dict()
            message['type'] = "getpub"
            message['user'] = "ALL"

            msg = pickle.dumps(message)
            msg = bytes(f"{len(msg):<10}", "utf-8") + msg
            s.send(msg)

            items = getData(s)

            self.updateSignal.emit(items)
            self.sleep(5)

    def stop(self):
        self.active = False
        self.wait()


class updateThreadFR(QtCore.QThread):
    updateSignal = QtCore.pyqtSignal(list)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.active = True

    def run(self):
        while self.active:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect(("127.0.0.1", 15000))
            except Exception:
                self.updateSignal.emit([])
                continue

            message = dict()
            message['type'] = "getf"
            message['user'] = currusr

            msg = pickle.dumps(message)
            msg = bytes(f"{len(msg):<10}", "utf-8") + msg
            s.send(msg)

            items = getData(s)

            self.updateSignal.emit(items)
            self.sleep(5)

    def stop(self):
        self.active = False
        self.wait()


class connListener(QtCore.QThread):
    updateSignal = QtCore.pyqtSignal(object)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.active = True

    def run(self):
        clnHost.listen(5)
        while self.active:
            cSock, cAddr = clnHost.accept()
            print(f"{cAddr} connected.")
            print(type(cAddr))

            self.updateSignal.emit(cSock)
    def stop(self):
        self.active = False
        clnHost.close()
        self.wait()

app = QApplication(sys.argv)
win = window()
win.show()
sys.exit(app.exec_())