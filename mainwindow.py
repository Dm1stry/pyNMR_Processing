import sys
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt6 import QtCore, QtGui, QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


from PyQt6 import uic
from processors import *
from data import *

class MPL_element:
    def __init__(self, title, *args, **kwargs):

        class MplCanvas(FigureCanvasQTAgg):
            def __init__(self, parent=None, width=5, height=4, dpi=100):
                self.fig = Figure(figsize=(width, height), dpi=dpi)
                self.axes = self.fig.add_subplot(111)
                self.axes.set_xlabel("T")
                self.axes.set_ylabel("A")
                self.fig.tight_layout()


                super(MplCanvas, self).__init__(self.fig)

            '''def __get_color(self):
                cmap = matplotlib.pyplot.get_cmap('jet_r')
                N = 10
                for i in range(N):
                    yield cmap(float(i)/N)'''
            def plot_draw(self, data_x, data_y):
                self.axes.scatter(data_x, data_y, s=0.5)
                self.fig.canvas.draw()

        class ToolButton(QtWidgets.QPushButton):
            def __init__(self, name: str, action, hint="", parent=None, *args, **kwargs):
                super().__init__(parent, *args, **kwargs)
                extension = '.svg'
                path = './src/mpl_tools/'
                full_path = path + name + extension
                icon = QtGui.QIcon(full_path)


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
                self.pan_toolbar_button = ToolButton('pan', self.toolbar.pan, hint="Левая кнопка мыши - Переместить\n"
                                                                                   "Правая - Увеличить\n")
                self.toolbar_layout.addWidget(self.pan_toolbar_button)
                self.zoom_toolbar_button = ToolButton('zoom', self.toolbar.zoom, hint="Увеличить выделенную область\n")
                self.toolbar_layout.addWidget(self.zoom_toolbar_button)
                self.subplots_toolbar_button = ToolButton('subplots', self.toolbar.configure_subplots, hint="Настройки графиков")
                self.toolbar_layout.addWidget(self.subplots_toolbar_button)
                self.settings_toolbar_button = ToolButton('settings', self.toolbar.edit_parameters, hint="Настройки отображения")
                self.toolbar_layout.addWidget(self.settings_toolbar_button)
                self.save_toolbar_button = ToolButton('save', self.toolbar.save_figure, hint="Сохранить в файл")
                self.toolbar_layout.addWidget(self.save_toolbar_button)

                spacer = QtWidgets.QSpacerItem(0, 40, vPolicy=QtWidgets.QSizePolicy.Policy.MinimumExpanding)
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
            self.__rescale(scale, 0))
        self.y_scale_box.textActivated.connect(
            lambda scale:
            self.__rescale(scale, 1))

    def __rescale(self, scale, axis):
        scales = {'Линейно': 'linear', 'Логарифмически': 'log'}
        if axis == 0:
            self.graph.axes.set_xscale(scales[scale])
            self.graph.fig.canvas.draw()
        else:
            self.graph.axes.set_yscale(scales[scale])
            self.graph.fig.canvas.draw()

class Processing_element:

    def __init__(self, processors, window):
        self.parent_window = window
        self.processors = processors
        self.layout = QtWidgets.QGridLayout()
        self.tikhonov_button = QtWidgets.QPushButton("Тихонов")
        self.tikhonov_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.Policy.Maximum)
        self.tikhonov_parameters_button = QtWidgets.QPushButton("...")
        self.tikhonov_parameters_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum,
                                           QtWidgets.QSizePolicy.Policy.Maximum)
        self.seq_search_button = QtWidgets.QPushButton("Посл. Поиск")
        self.seq_search_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.Policy.Maximum)
        self.seq_search_parameters_button = QtWidgets.QPushButton("...")
        self.tikhonov_parameters_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum,
                                                      QtWidgets.QSizePolicy.Policy.Maximum)

        self.layout.addWidget(self.tikhonov_button, 0, 0)
        self.layout.addWidget(self.tikhonov_parameters_button, 0, 1)
        self.layout.addWidget(self.seq_search_button, 1, 0)
        self.layout.addWidget(self.seq_search_parameters_button, 1, 1)

        self.tikhonov_button.clicked.connect(self.TikhonovProcess()) # <------- Не работает хоть убейся

    def TikhonovProcess(self):
        self.parent_window.print_log("Button clicked")

        class params:
            T_max = 1e9
            T_min = 1e-6
            iterations = int(1e4)

        self.parent_window.print_log("Processing started")
        self.processors[0].setParams(params)
        #self.processors[0].Process(window.data.get_data())
        self.parent_window.print_log("Processing ended")

        #return self.processors[0].getSpectrum()
        spectrum = self.processors[0].getSpectrum()
        window.spectrum_element.graph.axes.plot(spectrum[0], spectrum[1])
        window.print_log("Spectrum is ready")

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
        self.init_processing_interface()

        self.readSettings()

    def init_processing_interface(self):
        processing = Processing_element([TikhonovProcessor(), TikhonovProcessor()], self)
        self.process_layout.addLayout(processing.layout)


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
        self.print_log('path: ' + path)
        self.data.read(path)
        self.print_log('Данные прочитаны')
        t, A = self.data.get_data()
        self.plot_element.graph.plot_draw(t, A)

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


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
