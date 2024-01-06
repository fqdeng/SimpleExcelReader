from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication

import fire
import os
from common_window import SavePositionWindow
from main_window import Ui_SimpleExcelReader
from output_window import Ui_Output
import platform
import signal
import sys
import util
import pandas
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QTimer, QObject, pyqtSlot
from ace_editor import AceEditorWindow
import logging


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


class OutputWindow(SavePositionWindow, Ui_Output):
    def __init__(self, parent=None, main_window: MainWindow = None):
        super(OutputWindow, self).__init__(parent)
        self.setupUi(self)
        # set clicked event
        self.executeButton.clicked.connect(self.execute_code)
        self.saveCodeButton.clicked.connect(self.save_code)
        self.main_window = main_window
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.code = ""

    def execute_code(self):
        cxt = {'df': self.main_window.get_df(), 'window': self.main_window}
        logging.info(f"Execute code: {self.code}")
        self.plainTextEdit_2.setPlainText(
            util.eval_and_capture_output(self.code, context=cxt))
        self.main_window.render_df(cxt["df"])

    def save_code(self):
        with open('code', 'w') as file:
            file.write(self.code)


class EditorHandler(QObject):
    def __init__(self):
        super().__init__()
        self.editor_window = None

    @pyqtSlot(str)
    def onTextChanged(self, text):
        self.editor_window.code = text


class App(QObject):
    def __init__(self):
        super().__init__()
        self.ace_editor_window = None
        self.main_window = None

    def start(self, file_path=None):
        os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--disable-gpu'
        logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w',
                            format='%(name)s - %(levelname)s - %(message)s')
        app = QtWidgets.QApplication(sys.argv)
        main_window = MainWindow()
        main_window.show()
        main_window.open_excel(file_path)
        self.main_window = main_window

        handler = EditorHandler()
        ace_editor_window = AceEditorWindow(handler=handler)
        ace_editor_window.show()

        editor_window = OutputWindow(main_window=main_window)
        editor_window.show()
        handler.editor_window = editor_window
        self.ace_editor_window = ace_editor_window
        self._init_code()

        timer = QTimer()
        timer.start(500)  # You may change this if you wish.
        timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms.
        # Register the signal handler for Ctrl+C
        signal.signal(signal.SIGINT, util.signal_handler)

        sys.exit(app.exec_())

    def _init_code(self):
        # 创建 QTimer 对象
        self.timer = QTimer(self)
        # 设置定时器超时信号的回调函数
        self.timer.timeout.connect(self._init_editor)
        # 设置定时器的时间间隔（例如，1000 毫秒）
        self.timer.start(2000)

    def _init_editor(self):
        with open('code', 'r') as file:
            code = file.read()
            self.ace_editor_window.set_editor_text(code)
            self.timer.stop()


def windows_hidpi_support():
    if platform.system() == "Windows":
        QtCore.QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QtGui.QGuiApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)


def main(file_path='./data.xls'):
    App().start(file_path)


if __name__ == "__main__":
    windows_hidpi_support()
    fire.Fire(main)
