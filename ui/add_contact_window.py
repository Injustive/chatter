# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_contact.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddContactWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Ui_AddContactWindow")
        MainWindow.resize(423, 250)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.enter_name_label = QtWidgets.QLabel(self.centralwidget)
        self.enter_name_label.setGeometry(QtCore.QRect(120, 20, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.enter_name_label.setFont(font)
        self.enter_name_label.setObjectName("enter_name_label")
        self.ok_btn = QtWidgets.QPushButton(self.centralwidget)
        self.ok_btn.setGeometry(QtCore.QRect(120, 120, 75, 23))
        self.ok_btn.setObjectName("ok_btn")
        self.ok_btn.setDisabled(True)
        self.enter_name_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.enter_name_edit.setGeometry(QtCore.QRect(110, 60, 191, 41))
        self.enter_name_edit.setObjectName("entrer_name_edit")
        self.cancel_btn = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_btn.setGeometry(QtCore.QRect(210, 120, 75, 23))
        self.cancel_btn.setObjectName("cancel_btn")
        self.extra_label = QtWidgets.QLabel(self.centralwidget)
        self.extra_label.setGeometry(QtCore.QRect(110, 150, 220, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.extra_label.setFont(font)
        self.extra_label.setText("")
        self.extra_label.setObjectName("extra_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 423, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Add contact", "Add contact"))
        self.enter_name_label.setText(_translate("MainWindow", "Enter the contact login:"))
        self.ok_btn.setText(_translate("MainWindow", "Ok"))
        self.cancel_btn.setText(_translate("MainWindow", "Cancel"))
