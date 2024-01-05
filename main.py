from PyQt5.QtWidgets import QFileDialog

import syntax_pars
from main_window import Ui_SimpleExcelReader
from code_editor import Ui_PythonCodeEditor
import platform
import signal
import sys
import util
import pandas
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt


class MainWindow(QtWidgets.QMainWindow, Ui_SimpleExcelReader):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.actionOpen.triggered.connect(self.openFile)
        self.df = None

    def openFile(self):
        # Open a file dialog and set the filter to .xlsx files
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Excel Files (*.xlsx)", options=options)

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


class EditorWindow(QtWidgets.QMainWindow, Ui_PythonCodeEditor):
    def __init__(self, parent=None, main_window: MainWindow = None):
        super(EditorWindow, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setupUi(self)

        # set clicked event
        self.executeButton.clicked.connect(self.execute_code)
        self.main_window = main_window
        self.editor.set_tab_length(4)  # init the tab length to 4 spaces

    def execute_code(self):
        code = self.editor.toPlainText()
        print("execute:")
        print(code)
        cxt = {'df': self.main_window.get_df(), 'window': self.main_window}
        self.plainTextEdit_2.setPlainText(
            util.eval_and_capture_output(code, context=cxt))
        self.main_window.render_df(cxt["df"])


def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    df = mainWindow.open_excel('./data.xls')
    editorWindow = EditorWindow(main_window=mainWindow)
    editorWindow.show()
    mainWindowGeometry = mainWindow.frameGeometry()
    editorWindow.move(mainWindowGeometry.topRight())
    editor = editorWindow.editor
    editor.setStyleSheet("""QPlainTextEdit{
    	font-family:'Consolas'; 
    	color: #ccc; 
    	background-color: #2b2b2b;}""")
    highlight = syntax_pars.PythonHighlighter(editor.document())
    editor.show()
    # Load syntax.py into the editor for demo purposes
    infile = open('code', 'r')
    editor.setPlainText(infile.read())
    # Register the signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())


def windows_hidpi_support():
    if platform.system() == "Windows":
        QtCore.QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QtGui.QGuiApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)


if __name__ == "__main__":
    windows_hidpi_support()
    main()
