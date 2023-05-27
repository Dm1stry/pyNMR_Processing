from PyQt6 import QtCore, QtGui, QtWidgets, QtGui
from PyQt6 import uic

import sys

class TikhonovSettingsWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUi()

    def initUi(self):
        uic.loadUi("./tikhonov_settings_window.ui", self)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TikhonovSettingsWindow()
    window.show()
    app.exec()