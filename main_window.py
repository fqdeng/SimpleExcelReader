from __future__ import annotations
import pandas
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog

import util
from common_window import SavePositionWindow
from main_window_ui import Ui_SimpleExcelReader


class MainWindow(SavePositionWindow, Ui_SimpleExcelReader, QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.actionOpen.triggered.connect(self.openFile)
        self.df = None

    def openFile(self):
        # Open a file dialog and set the filter to .xlsx files
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Excel Files (*.xlsx *xls)", options=options)

        if filePath:
            print(filePath)  # Or handle the file path as needed
        self.open_excel(filePath)

    def open_excel(self, filePath):
        # table show some data from pandas read './jobs.xlsx'
        self.df = pandas.read_excel(filePath)
        self.render_df(self.df)
        return self.df

    def get_df(self):
        return self.df

    def render_df(self, df):
        self.df = df
        self.tableWidget.setRowCount(df.shape[0])
        self.tableWidget.setColumnCount(df.shape[1])
        header = df.columns.tolist()
        header = [str(item) for item in header]
        self.tableWidget.setHorizontalHeaderLabels(header)
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(df.iloc[i, j])))

    def closeEvent(self, event):
        super().closeEvent(event)
        util.close_app()
