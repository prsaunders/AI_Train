# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FileOpen.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dlgFileOpen(object):
    def setupUi(self, dlgFileOpen):
        dlgFileOpen.setObjectName("dlgFileOpen")
        dlgFileOpen.resize(350, 130)
        self.cbxFileList = QtWidgets.QComboBox(dlgFileOpen)
        self.cbxFileList.setGeometry(QtCore.QRect(100, 30, 231, 21))
        font = QtGui.QFont()
        font.setFamily("Piboto [Goog]")
        font.setPointSize(10)
        self.cbxFileList.setFont(font)
        self.cbxFileList.setInputMethodHints(QtCore.Qt.ImhMultiLine)
        self.cbxFileList.setEditable(False)
        self.cbxFileList.setMaxVisibleItems(9)
        self.cbxFileList.setObjectName("cbxFileList")
        self.label = QtWidgets.QLabel(dlgFileOpen)
        self.label.setGeometry(QtCore.QRect(20, 30, 71, 22))
        font = QtGui.QFont()
        font.setFamily("Piboto [Goog]")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.dlgbxFileOpen = QtWidgets.QDialogButtonBox(dlgFileOpen)
        self.dlgbxFileOpen.setGeometry(QtCore.QRect(70, 80, 261, 32))
        font = QtGui.QFont()
        font.setFamily("Piboto [Goog]")
        font.setPointSize(10)
        self.dlgbxFileOpen.setFont(font)
        self.dlgbxFileOpen.setOrientation(QtCore.Qt.Horizontal)
        self.dlgbxFileOpen.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.dlgbxFileOpen.setObjectName("dlgbxFileOpen")

        self.retranslateUi(dlgFileOpen)
        self.dlgbxFileOpen.accepted.connect(dlgFileOpen.accept)
        self.dlgbxFileOpen.rejected.connect(dlgFileOpen.reject)
        self.dlgbxFileOpen.clicked['QAbstractButton*'].connect(dlgFileOpen.accept)
        QtCore.QMetaObject.connectSlotsByName(dlgFileOpen)

    def retranslateUi(self, dlgFileOpen):
        _translate = QtCore.QCoreApplication.translate
        dlgFileOpen.setWindowTitle(_translate("dlgFileOpen", "File Open"))
        self.label.setText(_translate("dlgFileOpen", "Select File:"))

