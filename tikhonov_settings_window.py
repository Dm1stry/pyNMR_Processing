from PyQt6 import QtWidgets, QtGui
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
        self.alpha_edit.setText(str(self.params.alpha))
        self.T_min_edit.setText(str(self.params.T_min))
        self.T_max_edit.setText(str(self.params.T_max))
        self.iterations_edit.setText(str(self.params.iterations))
        self.p_size_edit.setText(str(self.params.p_size))
        onlyIntIterations = QtGui.QIntValidator()
        onlyIntIterations.setRange(20, 10000)
        self.iterations_edit.setValidator(onlyIntIterations)
        onlyIntP_size = QtGui.QIntValidator()
        onlyIntP_size.setRange(100, 10000)
        self.p_size_edit.setValidator(onlyIntP_size)



    def connect_slots(self):
        self.save_settings.clicked.connect(self.on_save_clicked)
        self.reset_settings.clicked.connect(self.on_cancel_clicked)
        self.default_settings.clicked.connect(self.on_default_clicked)
        self.alpha_edit.editingFinished.connect(lambda: self.on_alpha_changed(self.alpha_edit.text()))
        self.T_min_edit.editingFinished.connect(lambda: self.on_T_min_changed(self.T_min_edit.text()))
        self.T_max_edit.editingFinished.connect(lambda: self.on_T_max_changed(self.T_max_edit.text()))
        self.iterations_edit.editingFinished.connect(lambda: self.on_iterations_changed(self.iterations_edit.text()))
        self.p_size_edit.editingFinished.connect(lambda: self.on_p_size_changed(self.p_size_edit.text()))

    def on_save_clicked(self):
        self.mainwindow.tikhonov_processor.setParams(self.params)
        self.mainwindow.tikhonov_params.setParams(self.params)
        self.mainwindow.print_log(" ".join(["Новые значения сохранены:\n T_min =", str(self.params.T_min),
                                  "\n T_max =", str(self.params.T_max),
                                  "\n Количество итераций =", str(self.params.iterations),
                                  "\n Альфа =", str(self.params.alpha),
                                  "\n Дискретизация по времени =", str(self.params.p_size) + "\n"]))
        self.close()

    def on_cancel_clicked(self):
        self.close()

    def on_default_clicked(self):
        self.params = TikhonovParams()

# on_XXX_changed needed to add value verification
    def on_alpha_changed(self, new_alpha):
        try:
            alpha = float(new_alpha)
        except Exception:
            self.mainwindow.print_log("В поле \"Альфа\" введено некорректное значение, значение не изменено.")
        else:
            self.params.alpha = alpha

    def on_T_min_changed(self, new_T_min):
        try:
            T_min = float(new_T_min)
        except Exception:
            self.mainwindow.print_log("В поле \"T_min\" введено некорректное значение, значение не изменено.")
        else:
            self.params.T_min = T_min

    def on_T_max_changed(self, new_T_max):
        try:
            T_max = float(new_T_max)
        except Exception:
            self.mainwindow.print_log("В поле \"T_max\" введено некорректное значение, значение не изменено.")
        else:
            self.params.T_max = T_max


    def on_iterations_changed(self, new_iterations):
        try:
            iterations = int(new_iterations)
        except Exception:
            self.mainwindow.print_log("В поле \"Количество итераций\" введено некорректное значение,"
                                      " значение не изменено.")
        else:
            self.params.iterations = iterations

    def on_p_size_changed(self, new_p_size):
        try:
            p_size = int(new_p_size)
        except Exception:
            self.mainwindow.print_log("В поле \"Дискр. Времени\" введено некорректное значение,"
                                      " значение не изменено.")
        else:
            self.params.p_size = p_size