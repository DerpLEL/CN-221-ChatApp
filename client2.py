#Rebuild everything using PyQt5
import socket
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from login import Ui_Frame as loginFrame
from mainInterface import Ui_MainWindow
from register import Ui_Frame as regFrame
import pickle

currport = 5001
currusr = ""

def getData(sock):
    length_header = sock.recv(10)
    data_length = int(length_header.decode("utf-8").strip())
    msg = sock.recv(data_length)
    return pickle.loads(msg)

class registerWindow(QMainWindow, regFrame):
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

class window(QMainWindow, loginFrame):
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


class MainWin(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.clnlist = list()
        self.setWindowTitle(f"Logged in as {currusr}")

        self.listWidget.addItem(QListWidgetItem("Client 1"))
        self.listWidget.addItem(QListWidgetItem("Client 2"))
        self.listWidget.itemActivated.connect(self.doubleclicked)
        self.actionExit.triggered.connect(self.logout)

        self.updT = updateThread(self)
        self.updT.updateSignal.connect(self.updatelist)
        self.updT.start()

    def doubleclicked(self):
        self.listWidget.clear()

    def updatelist(self, items):
        items = [x for x in items if x[0] != currusr]
        self.clnlist = items

        # Where commit
        self.listWidget.clear()
        for item in self.clnlist:
            self.listWidget.addItem(QListWidgetItem(item[0]))

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

        self.loginWin = window()
        self.loginWin.show()

        self.updT.stop()
        self.close()


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
                mg = QMessageBox.critical(None, "Error", "Can't connect to server, please try again later.")
                self.active = False
                return

            message = dict()
            message['type'] = "getpub"

            msg = pickle.dumps(message)
            msg = bytes(f"{len(msg):<10}", "utf-8") + msg
            s.send(msg)

            items = getData(s)

            self.updateSignal.emit(items)
            self.sleep(5)

    def stop(self):
        self.active = False
        self.wait()


app = QApplication(sys.argv)
win = window()
win.show()
sys.exit(app.exec_())