# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CN-221-ChatApp/ui/chatUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(393, 600)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.find_friend_button = QtWidgets.QPushButton(self.centralwidget)
        self.find_friend_button.setGeometry(QtCore.QRect(340, 10, 51, 30))
        self.find_friend_button.setObjectName("find_friend_button")
        self.search_friend_box = QtWidgets.QLineEdit(self.centralwidget)
        self.search_friend_box.setGeometry(QtCore.QRect(10, 10, 321, 30))
        self.search_friend_box.setStyleSheet("QlineEdit{\n"
"boder: 2px solid rgb(0, 0, 50);\n"
"boder-radius: 20px;\n"
"color:#FFF\n"
"}")
        self.search_friend_box.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.search_friend_box.setObjectName("search_friend_box")
        self.FriendList = QtWidgets.QListView(self.centralwidget)
        self.FriendList.setGeometry(QtCore.QRect(9, 80, 371, 221))
        self.FriendList.setObjectName("FriendList")
        self.GroupList = QtWidgets.QListView(self.centralwidget)
        self.GroupList.setGeometry(QtCore.QRect(9, 340, 371, 200))
        self.GroupList.setObjectName("GroupList")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 60, 361, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 320, 361, 21))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 393, 21))
        self.menubar.setObjectName("menubar")
        self.menuLogout = QtWidgets.QMenu(self.menubar)
        self.menuLogout.setObjectName("menuLogout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLogout = QtWidgets.QAction(MainWindow)
        self.actionLogout.setObjectName("actionLogout")
        self.menuLogout.addAction(self.actionLogout)
        self.menubar.addAction(self.menuLogout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.find_friend_button.setText(_translate("MainWindow", "FIND"))
        self.search_friend_box.setPlaceholderText(_translate("MainWindow", "Type here to search your friends"))
        self.label.setText(_translate("MainWindow", "Friend list"))
        self.label_2.setText(_translate("MainWindow", "Group list"))
        self.menuLogout.setTitle(_translate("MainWindow", "Menu"))
        self.actionLogout.setText(_translate("MainWindow", "Logout"))

"""self.queryReq = ""
        self.setWindowTitle(f"Logged in as {currusr}")

        #self.FriendList.itemClicked.connect(self.test)
        #self.FriendList.addItem(QListWidgetItem("Placeholder"))
        self.actionLogout.triggered.connect(self.logout)

        self.search_friend_box.editingFinished.connect(self.setreq)
        self.find_friend_button.clicked.connect(self.openResWindow)

        #self.updT = updateThread(self)
        #self.updT.updateSignal.connect(self.updatelist)
        #self.updT.start()
    def test(self, item):
        print(item)
    def openResWindow(self):
        self.resWin = searchWindow(None, self.queryReq)
        self.resWin.show()

    def setreq(self):
        self.queryReq = self.search_friend_box.text()
    def updatelist(self, items):
        items = [x for x in items if x[0] != currusr]
        self.clnlist = items

        # Where commit
        self.FriendList.clear()
        for item in self.clnlist:
            self.FriendList.addItem(QListWidgetItem(item[0]))"""