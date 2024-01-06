from PyQt5.QtWidgets import QFileDialog

import syntax_pars, os
from common import SavePositionWindow
from main_window import Ui_SimpleExcelReader
from code_editor import Ui_PythonCodeEditor
import platform
import signal
import sys
import util
import pandas
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QTimer
from ace_editor import AceEditorWindow


class MainWindow(SavePositionWindow, Ui_SimpleExcelReader):
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


class EditorWindow(SavePositionWindow, Ui_PythonCodeEditor):
    def __init__(self, parent=None, main_window: MainWindow = None, ace_editor_window: AceEditorWindow = None):
        super(EditorWindow, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        # set clicked event
        self.executeButton.clicked.connect(self.execute_code)
        self.main_window = main_window
        self.ace_editor_window = ace_editor_window
        self.editor.set_tab_length(4)  # init the tab length to 4 spaces

        self.editor.setReadOnly(True)

        self.editor.setStyleSheet("""QPlainTextEdit{
            	font-family:'Consolas'; 
            	color: #ccc; 
            	background-color: #2b2b2b;}""")

        # Load syntax.py into the editor for demo purposes

        # 创建 QTimer 对象
        self.timer = QTimer(self)
        # 设置定时器超时信号的回调函数
        self.timer.timeout.connect(self.update_code)
        # 设置定时器的时间间隔（例如，1000 毫秒）
        self.timer.start(2000)

    def update_code(self):
        self.ace_editor_window.set_editor_text(self.editor.toPlainText())
        self.timer.stop()

    def execute_code(self):
        code = self.editor.toPlainText()
        print("execute:")
        print(code)
        cxt = {'df': self.main_window.get_df(), 'window': self.main_window}
        self.plainTextEdit_2.setPlainText(
            util.eval_and_capture_output(code, context=cxt))
        self.main_window.render_df(cxt["df"])

    def set_plain_text(self, text):
        self.editor.setPlainText(text)


class Handler:
    def __init__(self, editor_window: EditorWindow = None):
        self.editor_window = editor_window

    def handle(self, msg):
        print("Received message:", msg)
        self.editor_window.set_plain_text(msg)


def main():
    os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--disable-gpu'
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    main_window.open_excel('./data.xls')

    handler = Handler()
    ace_editor_window = AceEditorWindow()
    ace_editor_window.show()

    editor_window = EditorWindow(main_window=main_window, ace_editor_window=ace_editor_window)
    editor_window.show()
    handler.editor_window = editor_window

    init_editor(editor_window)
    # Register the signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())


def init_editor(editor_window: EditorWindow):
    infile = open('code', 'r')
    code = infile.read()
    highlight = syntax_pars.PythonHighlighter(editor_window.editor.document())
    editor_window.set_plain_text(code)


def windows_hidpi_support():
    if platform.system() == "Windows":
        QtCore.QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QtGui.QGuiApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)


if __name__ == "__main__":
    windows_hidpi_support()
    main()
