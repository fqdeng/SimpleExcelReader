import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow

_config_file_path = './config/config.json'


# save the position and size of the window
class SavePositionWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SavePositionWindow, self).__init__(parent)
        self.load_window_settings()

    def closeEvent(self, event):
        self.save_window_settings()
        super().closeEvent(event)

    def save_window_settings(self):
        window_settings = {
            'size': [self.width(), self.height()],
            'position': [self.x(), self.y()]
        }
        with open(_config_file_path, 'r+') as file:
            config = json.load(file)
            config[self.__class__.__name__] = window_settings
            file.seek(0)  # Reset file position to the beginning.
            json.dump(config, file, indent=4)
            file.truncate()  # Remove remaining part of old data

    def load_window_settings(self):
        try:
            with open(_config_file_path, 'r') as file:
                config = json.load(file)
                settings = config.get(self.__class__.__name__, {})
                size = settings.get('size', [400, 300])
                position = settings.get('position', [100, 100])
                self.resize(*size)
                self.move(*position)
        except FileNotFoundError:
            # If config file doesn't exist, create one with default settings.
            with open(_config_file_path, 'w') as file:
                json.dump({}, file)
