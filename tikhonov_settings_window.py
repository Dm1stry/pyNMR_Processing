from PyQt6 import QtWidgets
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
        self.alpha_edit.textChanged.connect(self.on_alpha_changed)  # Change to OnEnter, cause app crashes on values with e
        self.T_min_edit.textChanged.connect(self.on_T_min_changed)
        self.T_max_edit.textChanged.connect(self.on_T_max_changed)
        self.iterations_edit.textChanged.connect(self.on_iterations_changed)
        self.p_size_edit.textChanged.connect(self.on_p_size_changed)

    def on_save_clicked(self):
        self.mainwindow.tikhonov_processor.setParams(self.params)
        self.mainwindow.tikhonov_params.setParams(self.params)
        '''self.mainwindow.print_log(" ".join(["Новые значения сохранены:\n T_min =", self.params.T_min,
                                  "\n T_max =", self.params.T_max,
                                  "\n Количество итераций =", self.params.iterations,
                                  "\n Альфа =", self.params.alpha,
                                  "\n Дискретизация по времени =", self.params.p_size]))'''
        self.close()

    def on_cancel_clicked(self):
        self.close()

# on_XXX_changed needed to add value verification
    def on_alpha_changed(self, new_alpha):
        self.params.alpha = float(new_alpha)

    def on_T_min_changed(self, new_T_min):
        self.params.T_min = float(new_T_min)

    def on_T_max_changed(self, new_T_max):
        self.params.T_max = float(new_T_max)

    def on_iterations_changed(self, new_iterations):
        self.params.iterations = int(new_iterations)

    def on_p_size_changed(self, new_p_size):
        self.params.p_size = int(new_p_size)