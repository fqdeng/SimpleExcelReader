# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'output_window_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Output(object):
    def setupUi(self, Output):
        Output.setObjectName("Output")
        self.centralwidget = QtWidgets.QWidget(Output)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.executeButton = QtWidgets.QPushButton(self.centralwidget)
        self.executeButton.setObjectName("executeButton")
        self.horizontalLayout.addWidget(self.executeButton)
        self.saveCodeButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveCodeButton.setObjectName("saveCodeButton")
        self.horizontalLayout.addWidget(self.saveCodeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.outputTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.outputTextEdit.setObjectName("outputTextEdit")
        self.verticalLayout.addWidget(self.outputTextEdit)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 15)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        Output.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Output)
        self.statusbar.setObjectName("statusbar")
        Output.setStatusBar(self.statusbar)

        self.retranslateUi(Output)
        QtCore.QMetaObject.connectSlotsByName(Output)

    def retranslateUi(self, Output):
        _translate = QtCore.QCoreApplication.translate
        Output.setWindowTitle(_translate("Output", "Output"))
        self.executeButton.setText(_translate("Output", "Execute"))
        self.saveCodeButton.setText(_translate("Output", "SaveCode"))
