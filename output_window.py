from __future__ import annotations

import logging

from PyQt5 import QtCore
from PyQt5.QtCore import Qt

import util
from app import App
from common_window import SavePositionWindow
from main_window import MainWindow
from output_window_ui import Ui_Output


class OutputWindow(SavePositionWindow, Ui_Output):
    def __init__(self, parent=None, main_window: MainWindow = None, app: App = None):
        super(OutputWindow, self).__init__(parent)
        self.statusbar = self.statusBar()
        self.app = app
        self.setupUi(self)
        # set clicked event
        self.executeButton.clicked.connect(self.execute_code)
        self.saveCodeButton.clicked.connect(self.save_code)
        self.main_window = main_window
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        self.statusr_bar_timer = QtCore.QTimer()
        self.statusr_bar_timer.timeout.connect(self.clear_status_bar)

    def clear_status_bar(self):
        self.statusbar.clearMessage()
        self.statusr_bar_timer.stop()

    def show_message_on_status_bar(self, msg):
        self.statusbar.showMessage("Status: " + msg)
        self.statusr_bar_timer.start(1000)

    def execute_code(self):
        cxt = {'df': self.main_window.get_df(), 'window': self.main_window}
        logging.info(f"Execute code: {self.app.code}")
        self.plainTextEdit_2.setPlainText(
            util.eval_and_capture_output(self.app.code, context=cxt))
        self.main_window.render_df(cxt["df"])
        self.show_message_on_status_bar("Code Executed.")

    def save_code(self):
        logging.info(f"Save code: {self.app.code}")
        self.app.save_code()
        self.show_message_on_status_bar("Code Saved.")
