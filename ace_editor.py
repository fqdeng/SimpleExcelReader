from __future__ import annotations

import json
import logging
import os

from PyQt5 import QtCore
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl, QObject, pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

import util
from app import App
from common_window import SavePositionWindow

_main_index_html_path = "./config/index.html"
real_index = "./config/main.html"


class AceEditorHandler(QObject):
    def __init__(self, app: App, ace_editor: AceEditorWindow):
        super().__init__()
        self.app = app
        self.ace_editor = ace_editor

    @pyqtSlot(str)
    def onTextChanged(self, text):
        self.app.code = text

    @pyqtSlot()
    def onEditorInit(self):
        logging.debug(f"Editor init")
        self.app.init_editor()
        self.ace_editor.resize_ace_editor()

    @pyqtSlot(str, list)
    def onCommand(self, command, args: list):
        logging.debug(f"Editor command: {command} {args}")
        if command == "write":
            logging.debug(f"Editor save")
            if len(args) > 0:
                self.app.output_window.save_code(file_path=args[0])
            else:
                self.app.output_window.save_code()

        if command == "edit":
            logging.debug(f"Editor open file")
            if len(args) > 0:
                logging.debug(f"Editor open file: {args[0]}")
                self.app.init_editor(file_path=args[0])
                self.app.code_path = args[0]

        if command == "ls":
            logging.debug(f"Show file list")
            file_list = []
            if len(args) > 0:
                logging.debug(f"Show file list: {args[0]}")
                file_list = util.list_files_and_directories(args[0])
            else:
                file_list = util.list_files_and_directories(os.getcwd())
            js_code = f"page.renderFileList({json.dumps(file_list)})"
            self.ace_editor.run_js_code(js_code)

        if command == "execute":
            self.app.output_window.execute_code()

        if command == "quit":
            util.close_app()


class CustomWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, line, sourceID):
        logging.debug(f"JS: {message} (Line: {line} Source: {sourceID})")


class AceEditorWindow(SavePositionWindow):
    def __init__(self, app: App = None, debug=False):
        super().__init__()
        self.dev_tools_view = None
        self.dev_tools_window = None
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Vim", "Vim"))
        self.app = app
        self.initUI()
        # self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        if debug:
            self.show_dev_tools()

    def initUI(self):
        self.browser = QWebEngineView(self)
        self.browser.setPage(CustomWebEnginePage(self.browser))

        self.setCentralWidget(self.browser)

        self.channel = QWebChannel(self.browser.page())
        self.ace_editor_handler = AceEditorHandler(self.app, self)
        self.channel.registerObject("editorHandler", self.ace_editor_handler)
        self.browser.page().setWebChannel(self.channel)

        self.setCentralWidget(self.browser)

        self.init_html_width_and_height()

        file_path = os.path.abspath(os.path.join(os.getcwd(), real_index))
        logging.debug(file_path)
        local_url = QUrl.fromLocalFile(file_path)
        self.browser.load(local_url)

    def init_html_width_and_height(self):
        with open(_main_index_html_path, "r", encoding="utf-8") as f:
            html = f.read()
        with open(real_index, "w", encoding="utf-8") as f:
            html = html.replace("800px", f"{self.width()}px")
            html = html.replace("600px", f"{self.height()}px")
            f.write(html)

    def resizeEvent(self, event):
        # This code will be executed every time the window is resized
        new_size = event.size()
        logging.debug(f"{self.__class__} Window resized to: {new_size.width()}x{new_size.height()}")
        self.resize_ace_editor(new_size.width(), new_size.height())
        super().resizeEvent(event)  # Ensure the default handler runs too

    def resize_ace_editor(self, width=None, height=None):
        if width is None:
            width = self.width()
        if height is None:
            height = self.height()

        logging.debug(f"Resize ace editor to: {width}x{height}")
        js_code = f"""
        if (page){{
            page.resizeTheWindowSize({width},{height})
        }}
        """
        # Execute the JavaScript code
        self.run_js_code(js_code)

    def focus_on_ace_editor(self):
        js_code = f"""
        editor.focus()
        """
        # Execute the JavaScript code
        self.run_js_code(js_code)

    def run_js_code(self, js_code):
        self.browser.page().runJavaScript(js_code)

    def set_editor_text(self, value):
        # get the ace editor
        js_code = f"""
        editor.setValue({json.dumps(value)})
        """
        # Execute the JavaScript code
        self.run_js_code(js_code)
        self.focus_on_ace_editor()

    def show_dev_tools(self):
        # Create a separate window for developer tools
        self.dev_tools_window = SavePositionWindow()
        self.dev_tools_view = QWebEngineView()

        # Set the developer tools view as the central widget of the new window
        self.dev_tools_window.setCentralWidget(self.dev_tools_view)

        # Connect the current page to the dev tools
        self.browser.page().setDevToolsPage(self.dev_tools_view.page())

        # Show the developer tools window
        self.dev_tools_window.show()
