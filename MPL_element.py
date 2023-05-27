import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from PyQt6 import QtGui, QtWidgets

class MPL_element: # Matplotlib wisual interface functional elemen, contains canvas anv Vertical toolbar that use standart mpl functions
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
            self.graph.fig.canvas.draw() #