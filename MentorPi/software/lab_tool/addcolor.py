# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addcolor.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 120)
        Dialog.setMinimumSize(QtCore.QSize(300, 120))
        Dialog.setMaximumSize(QtCore.QSize(300, 120))
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(100, 30, 120, 34))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_cancel = QtWidgets.QPushButton(Dialog)
        self.pushButton_cancel.setGeometry(QtCore.QRect(30, 80, 99, 30))
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.pushButton_ok = QtWidgets.QPushButton(Dialog)
        self.pushButton_ok.setGeometry(QtCore.QRect(170, 80, 99, 30))
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.label_name = QtWidgets.QLabel(Dialog)
        self.label_name.setGeometry(QtCore.QRect(40, 40, 51, 17))
        self.label_name.setAlignment(QtCore.Qt.AlignCenter)
        self.label_name.setObjectName("label_name")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "add color"))
        self.pushButton_cancel.setText(_translate("Dialog", "取消"))
        self.pushButton_ok.setText(_translate("Dialog", "确定"))
        self.label_name.setText(_translate("Dialog", "名称"))

