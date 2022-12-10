#Rebuild everything using PyQt5
import socket
import sys
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from login import Ui_Frame as loginFrame
from mainInterface import Ui_MainWindow
from register import Ui_Frame as regFrame
import pickle

currport = 5000
curusr = ""

class registerWindow(QMainWindow, regFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Register")
        self.usr = ""
        self.p1 = ""
        self.p2 = ""

        self.pushButton.clicked.connect(self.regchecksend)

        self.lineEdit.editingFinished.connect(self.getusrname)
        self.lineEdit_2.editingFinished.connect(self.getp1)
        self.lineEdit_3.editingFinished.connect(self.getp2)

    def regchecksend(self):
        if self.usr == "" or self.p1 == "" or self.p2 == "" or self.p1 != self.p2:
            mg = QMessageBox.critical(self, "Error", "Invalid credentials, please try again.")
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
            msg = bytes(f"{len(msg):<{10}}", "utf-8") + msg
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

        self.pushButton_2.clicked.connect(self.getmainwin)
        self.pushButton.clicked.connect(self.openreg)

        self.lineEdit.editingFinished.connect(self.setusrname)
        self.lineEdit_2.editingFinished.connect(self.setpass)

    def getmainwin(self):
        self.newWin = MainWin()
        self.newWin.show()
        self.close()

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
        list1 = self.listWidget
        self.setWindowTitle("Main Menu")
        list1.addItem(QListWidgetItem("Client 1"))
        list1.addItem(QListWidgetItem("Client 2"))
        list1.itemActivated.connect(self.doubleclicked)

        self.updT = updateThread(self)
        self.updT.updateSignal.connect(self.updatelist)
        self.updT.start()

    def doubleclicked(self):
        self.listWidget.clear()

    def updatelist(self, items):
        self.listWidget.clear()
        for item in items:
            self.listWidget.addItem(QListWidgetItem(item))


class updateThread(QtCore.QThread):
    updateSignal = QtCore.pyqtSignal(list)
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        while True:
            items = ["Client 1", "Client 2", "Client 3", "Client 4"]
            self.updateSignal.emit(items)
            self.sleep(15)



def window1():
    app = QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec_())

window1()