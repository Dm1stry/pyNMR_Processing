import sys
from multiprocessing import Pool, Process

from PyQt6 import QtCore, QtGui, QtWidgets, QtGui
from PyQt6 import uic

from data import *
from MPL_element import MPL_element
from tikhonov_settings_window import TikhonovSettingsWindow
from tikhonov_processor import TikhonovProcessor, TikhonovParams


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_data = ''
        self.data = Data()
        self.initUi()

    def initUi(self):
        uic.loadUi("./mainwindow.ui", self)

        self.setDockNestingEnabled(True)  # Allows widgets docks side by side
        self.takeCentralWidget()  # Removes central widget of window

        self.init_log()
        self.init_plot()
        self.init_spectrum()
        self.init_filesystem_widget()
        self.init_processing_element()

        self.readSettings()

    def init_filesystem_widget(self):
        self.tree = QtWidgets.QTreeView()
        self.dir_path_layout = QtWidgets.QHBoxLayout()
        self.dir_path_edit = QtWidgets.QLineEdit()
        self.dir_path_edit.setText(QtCore.QDir.currentPath())
        self.dir_path_edit.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding,
                                    QtWidgets.QSizePolicy.Policy.Maximum)
        dir_path_button = QtWidgets.QPushButton("Выбрать")
        dir_path_open_explorer_button = QtWidgets.QPushButton("...")
        dir_path_open_explorer_button.setMaximumWidth(20)
        dir_path_open_explorer_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum,
                                                    QtWidgets.QSizePolicy.Policy.Maximum)
        self.dir_path_layout.addWidget(self.dir_path_edit)
        self.dir_path_layout.addWidget(dir_path_open_explorer_button)
        self.dir_path_layout.addWidget(dir_path_button)
        self.filesystem_layout.addLayout(self.dir_path_layout)
        self.filesystem_layout.addWidget(self.tree)
        self.model = QtGui.QFileSystemModel()
        self.model.setRootPath(QtCore.QDir.currentPath())
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QtCore.QDir.currentPath()))

        self.tree.clicked.connect(self.on_filesystem_clicked)
        dir_path_open_explorer_button.clicked.connect(self.on_dir_path_open_explorer_button_clicked)
        dir_path_button.clicked.connect(self.on_dir_path_button_clicked)

    def on_filesystem_clicked(self, index):
        path = self.sender().model().filePath(index)
        self.print_log('path: ' + path)
        self.data.read(path)
        self.print_log('Данные прочитаны')
        t, A = self.data.get_data()
        self.plot_element.graph.plot_draw(t, A)

    def on_dir_path_open_explorer_button_clicked(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
        if dialog.exec():
            self.dir_path_edit.setText(str(dialog.selectedFiles()[0]))

    def on_dir_path_button_clicked(self):
        self.model.setRootPath(self.dir_path_edit.text())
        self.tree.setRootIndex(self.model.index(self.dir_path_edit.text()))

    def init_plot(self):
        self.plot_element = MPL_element("График")
        self.plot_element.graph.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        self.plot_layout.addLayout(self.plot_element.layout)

    def init_spectrum(self):
        self.spectrum_element = MPL_element("Спектр")
        self.spectrum_element.graph.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        self.spectrum_layout.addLayout(self.spectrum_element.layout)

    def init_log(self):
        self.print_log('Лог запущен')

    def init_processing_element(self):
        self.tikhonov_processor = TikhonovProcessor()
        self.tikhonov_params = TikhonovParams()
        self.tikhonov_button.clicked.connect(self.on_tikhonov_process_clicked)
        print(self.tikhonov_params.alpha)
        self.tikhonov_settings = TikhonovSettingsWindow(self.tikhonov_params, self)
        self.tikhonov_params_button.clicked.connect(self.tikhonov_settings.show)
        self.log_reg_button.clicked.connect(lambda: print(self.tikhonov_params.alpha))

    def on_tikhonov_process_clicked(self):
        self.tikhonov_processor.Process(self.data)
        curve_t, curve_A = self.tikhonov_processor.getCurve()
        spectrum_t, spectrum_A = self.tikhonov_processor.getSpectrum()
        print("Plotting started")
        self.plot_element.graph.plot_draw(curve_t, curve_A)
        self.spectrum_element.graph.plot_draw(spectrum_t, spectrum_A)

    def print_log(self, text):
        out = QtCore.QDateTime.toString(QtCore.QDateTime.currentDateTime()) + '\t' + str(text) + '\n'
        self.log_data += out
        self.log.insertPlainText(out)

    def closeEvent(self, event):
        print('closing')
        with open('Log.txt', 'w') as f:
            print(self.log_data, file=f)
        settings = QtCore.QSettings("./settings.ini", QtCore.QSettings.Format.IniFormat)
        settings.setValue('geometry', self.saveGeometry())
        settings.setValue('windowState', self.saveState())
        super(MainWindow, self).closeEvent(event)

    def readSettings(self):
        settings = QtCore.QSettings("./settings.ini", QtCore.QSettings.Format.IniFormat)
        if settings.value("geometry") is not None:
            self.restoreGeometry(settings.value("geometry"))
        if settings.value("windowState") is not None:
            self.restoreState(settings.value("windowState"))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
