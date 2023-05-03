import sys
import matplotlib
from copy import deepcopy
matplotlib.use('QtAgg')
from PyQt6 import QtCore, QtGui, QtWidgets, QtGui, Qt6
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


from PyQt6 import uic
from processors import *
from data import *
import os

class MPL_element:
    def __init__(self, title, *args, **kwargs):

        class MplCanvas(FigureCanvasQTAgg):
            def __init__(self, parent=None, width=5, height=4, dpi=100):
                self.fig = Figure(figsize=(width, height), dpi=dpi)
                self.axes = self.fig.add_subplot(111)
                super(MplCanvas, self).__init__(self.fig)

        class ToolButton(QtWidgets.QPushButton):
            def __init__(self, name: str, action, hint="", parent=None, *args, **kwargs):
                super().__init__(parent, *args, **kwargs)
                extension = '.svg'
                path = './src/mpl_tools/'
                full_path = path + name + extension
                pixmap = QtGui.QPixmap(full_path)
                icon = QtGui.QIcon(pixmap)


                size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)

                self.setSizePolicy(size_policy)
                self.setIcon(icon)
                self.setToolTip(hint)

                self.clicked.connect(action)

        class VerticalToolbar(QtWidgets.QWidget):
            def __init__(self, canvas, parent=None):
                super().__init__(parent, *args, **kwargs)
                size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum,
                                                    QtWidgets.QSizePolicy.Policy.MinimumExpanding)

                self.setSizePolicy(size_policy)
                self.toolbar = NavigationToolbar(canvas)
                self.toolbar.hide()
                self.toolbar_layout = QtWidgets.QVBoxLayout()
                self.home_toolbar_button = ToolButton('home', self.toolbar.home, hint="Восстановить исходный вид")
                self.toolbar_layout.addWidget(self.home_toolbar_button)
                self.back_toolbar_button = ToolButton('back', self.toolbar.back, hint="Вернуться на шаг назад")
                self.toolbar_layout.addWidget(self.back_toolbar_button)
                self.forward_toolbar_button = ToolButton('forward', self.toolbar.forward, hint="Восстановить отмененный шаг")
                self.toolbar_layout.addWidget(self.forward_toolbar_button)
                self.pan_toolbar_button = ToolButton('pan', self.toolbar.pan, hint="Левая кнопка мыши - переместить\n"
                                                                                   "Правая - увеличить\n"
                                                                                   "x/y - Зафиксировать ось\n"
                                                                                   "CTRL - зафиксировать вид")
                self.toolbar_layout.addWidget(self.pan_toolbar_button)
                self.zoom_toolbar_button = ToolButton('zoom', self.toolbar.zoom, hint="Увеличить выделенную область\n"
                                                                                      "x/y - Зафиксировать ось")
                self.toolbar_layout.addWidget(self.zoom_toolbar_button)
                self.subplots_toolbar_button = ToolButton('subplots', self.toolbar.configure_subplots, hint="Настройки графиков")
                self.toolbar_layout.addWidget(self.subplots_toolbar_button)
                self.settings_toolbar_button = ToolButton('settings', self.toolbar.edit_parameters, hint="Настройки отображения")
                self.toolbar_layout.addWidget(self.settings_toolbar_button)
                self.save_toolbar_button = ToolButton('save', self.toolbar.save_figure, hint="Сохранить в файл")
                self.toolbar_layout.addWidget(self.save_toolbar_button)


                spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
                self.toolbar_layout.addItem(spacer)
                self.setLayout(self.toolbar_layout)
                self.show()


        self.layout = QtWidgets.QVBoxLayout()
        self.graph_layout = QtWidgets.QHBoxLayout()
        self.graph = MplCanvas()

        self.toolbar = VerticalToolbar(self.graph)

        self.graph_layout.addWidget(self.graph)
        self.graph_layout.addWidget(self.toolbar)

        self.layout.addLayout(self.graph_layout)

        self.scale_layout = QtWidgets.QHBoxLayout()
        self.x_scale_box = QtWidgets.QComboBox()
        self.x_scale_box.addItems(['Линейно', 'Логарифмически'])
        self.x_label = QtWidgets.QLabel('X:')
        self.y_scale_box = QtWidgets.QComboBox()
        self.y_scale_box.addItems(['Линейно', 'Логарифмически'])
        self.y_label = QtWidgets.QLabel('Y:')
        self.scale_layout.addWidget(self.x_label)
        self.scale_layout.addWidget(self.x_scale_box)
        self.scale_layout.addWidget(self.y_label)
        self.scale_layout.addWidget(self.y_scale_box)
        horizontal_spacer = QtWidgets.QSpacerItem(40, 0, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        self.scale_layout.addItem(horizontal_spacer)
        self.layout.addLayout(self.scale_layout)

        self.x_scale_box.textActivated.connect(
            lambda scale:
            self.__rescale(self.graph.axes, scale, 0))
        self.y_scale_box.textActivated.connect(
            lambda scale:
            self.__rescale(self.graph.axes, scale, 1))


    def __rescale(self, graph, scale, axis):
        print("Масштаб:", scale)
        scales = {'Линейно': 'linear', 'Логарифмически': "log"}
        if axis == 0:
            graph.set_xscale(scales[scale])
        else:
            graph.set_yscale(scales[scale])


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_data = ''
        self.data = Data()
        self.initUi()
        self.Processor = TikhonovProcessor()

    def initUi(self):
        uic.loadUi("./mainwindow.ui", self)

        self.setDockNestingEnabled(True)  # Allows widgets docks side by side
        self.takeCentralWidget()  # Removes central widget of window

        self.init_log()
        self.init_plot()
        self.init_spectrum()
        self.init_filesystem_widget()

        self.readSettings()

    def init_filesystem_widget(self):
        tree = QtWidgets.QTreeView()
        self.filesystem_layout.addWidget(tree)
        model = QtGui.QFileSystemModel()
        model.setRootPath(QtCore.QDir.currentPath())
        tree.setModel(model)
        tree.setRootIndex(model.index(QtCore.QDir.currentPath()))
        tree.clicked.connect(self.on_filesystem_clicked)

    def on_filesystem_clicked(self, index):
        path = self.sender().model().filePath(index)
        self.print_log(('path:', path))
        self.data.read(path)
        self.print_log(('data прочитана:', self.data.get_data()))
        t, A = self.data.get_data()
        self.plot_element.graph.axes.plot(t, A)
        self.print_log(path)
        self.print_log("END FUCK YOU")

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

    def print_log(self, text):
        out = str(text) + '\t' + QtCore.QDateTime.toString(QtCore.QDateTime.currentDateTime()) + '\n'
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


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
