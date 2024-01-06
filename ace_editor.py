import sys, os

from PyQt5 import QtCore
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl, QObject, pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineScript

from common_window import SavePositionWindow


class AceEditorWindow(SavePositionWindow):
    def __init__(self, handler: QObject = None):
        super().__init__()
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Vim", "Vim"))
        self.initUI(handler)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)


    def initUI(self, handler):
        self.browser = QWebEngineView(self)
        self.setCentralWidget(self.browser)
        self.resize(800,429)

        self.channel = QWebChannel(self.browser.page())
        self.handler = handler
        self.channel.registerObject("editorHandler", self.handler)
        self.browser.page().setWebChannel(self.channel)

        self.setCentralWidget(self.browser)
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "index.html"))
        local_url = QUrl.fromLocalFile(file_path)
        self.browser.load(local_url)

    def resizeEvent(self, event):
        # This code will be executed every time the window is resized
        new_size = event.size()
        print(f"Window resized to: {new_size.width()}x{new_size.height()}")
        self.resize_ace_editor(new_size.width(), new_size.height())
        super().resizeEvent(event)  # Ensure the default handler runs too

    def resize_ace_editor(self, width, height):
        js_code = f"""
        e = document.getElementById('editor')
        e.style.width = '{width}px';
        e.style.height = '{height}px';
        """
        # Execute the JavaScript code
        self.browser.page().runJavaScript(js_code)

    def set_editor_text(self, value):
        # get the ace editor
        js_code = f"""
        editor.setValue(`{value}`)
        """
        # Execute the JavaScript code
        self.browser.page().runJavaScript(js_code)


if __name__ == '__main__':
    os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--disable-gpu'
    app = QApplication(sys.argv)
    mainWindow = AceEditorWindow()
    mainWindow.show()
    sys.exit(app.exec_())
