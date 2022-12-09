#Rebuild everything using PyQt5
import socket
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from login import Ui_Frame
from mainInterface import Ui_MainWindow
from register import Ui_Frame as regFrame
from PyQt5.uic import loadUi

s = socket.socket()

class registerWindow(QMainWindow, regFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Register")

        self.pushButton.clicked.connect(self.regchecksend)

    def regchecksend(self):
        print("lmao")


class window(QMainWindow, Ui_Frame):
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
        print(f"{self.usr}|{self.passw}")
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

    def doubleclicked(self):
        self.listWidget.addItem(QListWidgetItem("Nice"))


def window1():
    app = QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec_())

window1()