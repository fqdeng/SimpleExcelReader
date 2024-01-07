from __future__ import annotations

import fire
import os

import platform
import signal
import sys
import util
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QTimer, QObject
import logging


class App(QObject):
    def __init__(self):
        super().__init__()
        self.ace_editor_window = None
        self.main_window = None
        self.code = None

    def start(self, file_path=None):
        from main_window import MainWindow
        from output_window import OutputWindow
        from ace_editor import AceEditorWindow

        os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--disable-gpu'
        logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w',
                            format='%(name)s - %(levelname)s - %(message)s')
        app = QtWidgets.QApplication(sys.argv)
        main_window = MainWindow()
        main_window.show()
        main_window.open_excel(file_path)
        self.main_window = main_window

        ace_editor_window = AceEditorWindow(app=self)
        ace_editor_window.show()

        editor_window = OutputWindow(main_window=main_window, app=self)
        editor_window.show()

        self.ace_editor_window = ace_editor_window

        timer = QTimer()
        timer.start(500)  # You may change this if you wish.
        timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms.
        # Register the signal handler for Ctrl+C
        signal.signal(signal.SIGINT, util.signal_handler)

        sys.exit(app.exec_())


    def init_editor(self):
        with open('code', 'r') as file:
            self.code = file.read()
            self.ace_editor_window.set_editor_text(self.code)


def windows_hidpi_support():
    if platform.system() == "Windows":
        QtCore.QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QtGui.QGuiApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)


def main(file_path='./data.xls'):
    App().start(file_path)


if __name__ == "__main__":
    windows_hidpi_support()
    fire.Fire(main)
