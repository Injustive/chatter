# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLineEdit


class Ui_RegisterWindow(object):
    def setupUi(self, RegisterWindow):
        RegisterWindow.setObjectName("RegisterWindow")
        RegisterWindow.resize(814, 477)
        self.centralwidget = QtWidgets.QWidget(RegisterWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.last_name_lbl = QtWidgets.QLabel(self.centralwidget)
        self.last_name_lbl.setGeometry(QtCore.QRect(370, 250, 81, 16))
        self.last_name_lbl.setObjectName("label_3")
        self.first_name_lbl = QtWidgets.QLabel(self.centralwidget)
        self.first_name_lbl.setGeometry(QtCore.QRect(370, 190, 81, 16))
        self.first_name_lbl.setObjectName("label_4")
        self.passEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.passEdit.setGeometry(QtCore.QRect(320, 150, 151, 31))
        self.passEdit.setObjectName("lineEdit_2")
        self.passEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_lbl = QtWidgets.QLabel(self.centralwidget)
        self.login_lbl.setGeometry(QtCore.QRect(380, 70, 47, 13))
        self.login_lbl.setObjectName("label")
        self.register_btn = QtWidgets.QPushButton(self.centralwidget)
        self.register_btn.setGeometry(QtCore.QRect(330, 320, 131, 41))
        self.register_btn.setObjectName("pushButton")
        self.register_btn.setDisabled(True)
        self.loginEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.loginEdit.setGeometry(QtCore.QRect(320, 90, 151, 31))
        self.loginEdit.setObjectName("lineEdit")
        self.pass_lbl = QtWidgets.QLabel(self.centralwidget)
        self.pass_lbl.setGeometry(QtCore.QRect(370, 130, 81, 16))
        self.pass_lbl.setObjectName("label_2")
        self.firstNameEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.firstNameEdit.setGeometry(QtCore.QRect(320, 210, 151, 31))
        self.firstNameEdit.setText("")
        self.firstNameEdit.setObjectName("lineEdit_3")
        self.lastNameEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lastNameEdit.setGeometry(QtCore.QRect(320, 270, 151, 31))
        self.lastNameEdit.setText("")
        self.lastNameEdit.setObjectName("lineEdit_4")
        RegisterWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RegisterWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 814, 21))
        self.menubar.setObjectName("menubar")
        RegisterWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(RegisterWindow)
        self.statusbar.setObjectName("statusbar")
        RegisterWindow.setStatusBar(self.statusbar)
        self.extra_label = QtWidgets.QLabel(self.centralwidget)
        self.extra_label.setGeometry(QtCore.QRect(251, 370, 280, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.extra_label.setFont(font)
        self.extra_label.setStyleSheet("color: green")
        self.extra_label.setText("")
        self.extra_label.setObjectName("extra_label")
        self.retranslateUi(RegisterWindow)
        QtCore.QMetaObject.connectSlotsByName(RegisterWindow)

    def retranslateUi(self, RegisterWindow):
        _translate = QtCore.QCoreApplication.translate
        RegisterWindow.setWindowTitle(_translate("Registration", "Registration"))
        self.last_name_lbl.setText(_translate("RegisterWindow", "LAST NAME"))
        self.first_name_lbl.setText(_translate("RegisterWindow", "FIRST NAME"))
        self.login_lbl.setText(_translate("RegisterWindow", "LOGIN"))
        self.register_btn.setText(_translate("RegisterWindow", "REGISTER"))
        self.pass_lbl.setText(_translate("RegisterWindow", "PASSWORD"))