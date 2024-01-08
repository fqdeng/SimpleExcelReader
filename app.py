from __future__ import annotations

import fire
import os
import sys

import platform
import signal
import util
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QTimer, QObject
import logging

_default_code_path = "./config/code"


class App(QObject):
    def __init__(self):
        super().__init__()
        self.ace_editor_window = None
        self.main_window = None
        self.output_window = None
        self.code = None
        self.code_path = _default_code_path

    def save_code(self, code=None, file_path=None):
        if file_path is None or file_path is False:
            file_path = self.code_path
        with open(file_path, 'w') as file:
            if code is not None:
                file.write(code)
            else:
                file.write(self.code)

    def start(self, file_path=None, debug=False):
        from main_window import MainWindow
        from output_window import OutputWindow
        from ace_editor import AceEditorWindow

        os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--disable-gpu'
        util.init_logging_config(debug=debug)

        app = QtWidgets.QApplication(sys.argv)
        main_window = MainWindow()
        main_window.show()
        main_window.open_excel(file_path)
        self.main_window = main_window

        ace_editor_window = AceEditorWindow(app=self, debug=debug)
        ace_editor_window.show()

        output_window = OutputWindow(main_window=main_window, app=self)
        output_window.show()
        self.output_window = output_window
        self.ace_editor_window = ace_editor_window
        self.ace_editor_window.activateWindow()
        self.ace_editor_window.browser.setFocus()

        self.timer = QTimer()
        self.timer.start(500)  # You may change this if you wish.
        self.timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms.
        # Register the signal handler for Ctrl+C
        signal.signal(signal.SIGINT, util.signal_handler)

        sys.exit(app.exec_())

    def init_editor(self, file_path=_default_code_path):
        with open(file_path, 'r') as file:
            self.code = file.read()
            self.ace_editor_window.set_editor_text(self.code)


def windows_hidpi_support():
    if platform.system() == "Windows":
        QtCore.QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QtGui.QGuiApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)


def main(file_path='./config/data.xls', debug=False):
    App().start(file_path, debug)


if __name__ == "__main__":
    windows_hidpi_support()
    fire.Fire(main)
