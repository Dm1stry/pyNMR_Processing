from PyQt6 import QtCore, QtGui, QtWidgets, QtGui
from PyQt6 import uic

from tikhonov_processor import TikhonovParams

import sys


class TikhonovSettingsWindow(QtWidgets.QWidget):
    def __init__(self, params, mainwindow, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params = params
        self.mainwindow = mainwindow
        self.initUi()

    def initUi(self):
        uic.loadUi("./tikhonov_settings_window.ui", self)
        self.connect_slots()

    def connect_slots(self):
        self.save_settings.clicked.connect(self.on_save_clicked)
        self.reset_settings.clicked.connect(self.on_cancel_clicked)
        self.alpha_edit.textChanged.connect(self.on_alpha_changed)
        self.T_min_edit.textChanged.connect(self.on_T_min_changed)
        self.T_max_edit.textChanged.connect(self.on_T_max_changed)

    def on_save_clicked(self):
        self.mainwindow.tikhonov_processor.setParams(self.params)
        self.mainwindow.tikhonov_params.setParams(self.params)
        self.close()

    def on_cancel_clicked(self):
        self.close()

    def on_alpha_changed(self, new_alpha):
        self.params.alpha = new_alpha

    def on_T_min_changed(self, new_T_min):
        self.params.T_min = new_T_min

    def on_T_max_changed(self, new_T_max):
        self.params.T_max = new_T_max