from __future__ import annotations
import logging
import sys, os

from PyQt5 import QtCore
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl, QObject, pyqtSlot, Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

import util
from app import App
from common_window import SavePositionWindow


class AceEditorHandler(QObject):
    def __init__(self, app: App, ace_editor: AceEditorWindow):
        super().__init__()
        self.app = app
        self.ace_editor = ace_editor

    @pyqtSlot(str)
    def onTextChanged(self, text):
        logging.info(f"Text changed: {text}")
        self.app.code = text

    @pyqtSlot()
    def onEditorInit(self):
        logging.info(f"Editor init")
        self.ace_editor.resize_ace_editor()
        self.app.init_editor()

    @pyqtSlot(str, list)
    def onCommand(self, command, args: list):
        logging.info(f"Editor command: {command} {args}")
        if command == "write":
            logging.info(f"Editor save")
            if len(args) > 0:
                self.app.save_code(file_path=args[0])
            else:
                self.app.save_code()

        if command == "edit":
            logging.info(f"Editor open file")
            if len(args) > 0:
                logging.info(f"Editor open file: {args[0]}")
                self.app.init_editor(file_path=args[0])
                self.app.code_path = args[0]

        if command == "ls":
            logging.info(f"Show file list")
            if len(args) > 0:
                logging.info(f"Show file list: {args[0]}")
                file_list = util.list_files_and_directories(args[0])
            else:
                file_list = util.list_files_and_directories(os.getcwd())
            args = []
            for item in file_list:
                args.append(f'"{item}"')
            js_code = f"page.renderFileList([{','.join(args)}])"
            self.ace_editor.run_js_code(js_code)


class CustomWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, line, sourceID):
        logging.info(f"JS: {message} (Line: {line} Source: {sourceID})")


class AceEditorWindow(SavePositionWindow):
    def __init__(self, app: App = None, debug=False):
        super().__init__()
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Vim", "Vim"))
        self.app = app
        self.initUI()
        # self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        if debug:
            self.showDevTools()

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

        file_path = os.path.abspath(os.path.join(os.getcwd(), "index.html"))
        logging.info(file_path)
        local_url = QUrl.fromLocalFile(file_path)
        self.browser.load(local_url)

    def init_html_width_and_height(self):
        with open("./index.html", "r") as f:
            html = f.read()
        with open("./index.html", "w") as f:
            html = html.replace("800px", f"{self.width()}px")
            html = html.replace("600px", f"{self.height()}px")
            f.write(html)

    def resizeEvent(self, event):
        # This code will be executed every time the window is resized
        new_size = event.size()
        logging.info(f"{self.__class__} Window resized to: {new_size.width()}x{new_size.height()}")
        self.resize_ace_editor(new_size.width(), new_size.height())
        super().resizeEvent(event)  # Ensure the default handler runs too

    def resize_ace_editor(self, width=None, height=None):
        if width is None:
            width = self.width()
        if height is None:
            height = self.height()

        logging.info(f"Resize ace editor to: {width}x{height}")
        js_code = f"""
        if (page){{
            page.resizeTheWindowSize({width},{height})
        }}
        """
        # Execute the JavaScript code
        self.run_js_code(js_code)

    def run_js_code(self, js_code):
        self.browser.page().runJavaScript(js_code)

    def set_editor_text(self, value):
        # get the ace editor
        js_code = f"""
        editor.setValue(`{value}`)
        """
        # Execute the JavaScript code
        self.run_js_code(js_code)

    def showDevTools(self):
        # Create a separate window for developer tools
        self.devToolsWindow = QMainWindow()
        self.devToolsView = QWebEngineView()

        # Set the developer tools view as the central widget of the new window
        self.devToolsWindow.setCentralWidget(self.devToolsView)

        # Connect the current page to the dev tools
        self.browser.page().setDevToolsPage(self.devToolsView.page())

        # Show the developer tools window
        self.devToolsWindow.show()
