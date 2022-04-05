# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FileSave.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dlgFileSave(object):
    def setupUi(self, dlgFileSave):
        dlgFileSave.setObjectName("dlgFileSave")
        dlgFileSave.resize(350, 130)
        self.dlgbxAcelaStPt = QtWidgets.QDialogButtonBox(dlgFileSave)
        self.dlgbxAcelaStPt.setGeometry(QtCore.QRect(70, 80, 261, 32))
        font = QtGui.QFont()
        font.setFamily("Piboto [Goog]")
        font.setPointSize(10)
        self.dlgbxAcelaStPt.setFont(font)
        self.dlgbxAcelaStPt.setOrientation(QtCore.Qt.Horizontal)
        self.dlgbxAcelaStPt.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.dlgbxAcelaStPt.setObjectName("dlgbxAcelaStPt")
        self.cbxFileList = QtWidgets.QComboBox(dlgFileSave)
        self.cbxFileList.setGeometry(QtCore.QRect(100, 30, 231, 21))
        font = QtGui.QFont()
        font.setFamily("Piboto [Goog]")
        font.setPointSize(10)
        self.cbxFileList.setFont(font)
        self.cbxFileList.setInputMethodHints(QtCore.Qt.ImhMultiLine)
        self.cbxFileList.setObjectName("cbxFileList")
        self.label = QtWidgets.QLabel(dlgFileSave)
        self.label.setGeometry(QtCore.QRect(20, 30, 71, 22))
        font = QtGui.QFont()
        font.setFamily("Piboto [Goog]")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")

        self.retranslateUi(dlgFileSave)
        QtCore.QMetaObject.connectSlotsByName(dlgFileSave)

    def retranslateUi(self, dlgFileSave):
        _translate = QtCore.QCoreApplication.translate
        dlgFileSave.setWindowTitle(_translate("dlgFileSave", "File Save"))
        self.label.setText(_translate("dlgFileSave", "Select File:"))

