# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SimpleExcelReader.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SimpleExcelReader(object):
    def setupUi(self, SimpleExcelReader):
        SimpleExcelReader.setObjectName("SimpleExcelReader")
        self.centralwidget = QtWidgets.QWidget(SimpleExcelReader)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 811, 1000))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        SimpleExcelReader.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SimpleExcelReader)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 797, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        SimpleExcelReader.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SimpleExcelReader)
        self.statusbar.setObjectName("statusbar")
        SimpleExcelReader.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(SimpleExcelReader)
        self.actionOpen.setObjectName("actionOpen")
        self.menuFile.addAction(self.actionOpen)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(SimpleExcelReader)
        QtCore.QMetaObject.connectSlotsByName(SimpleExcelReader)

    def retranslateUi(self, SimpleExcelReader):
        _translate = QtCore.QCoreApplication.translate
        SimpleExcelReader.setWindowTitle(_translate("SimpleExcelReader", "SimpleExcelReader"))
        self.menuFile.setTitle(_translate("SimpleExcelReader", "File"))
        self.actionOpen.setText(_translate("SimpleExcelReader", "Open"))
