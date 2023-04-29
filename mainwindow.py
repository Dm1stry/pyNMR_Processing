import sys
import matplotlib
matplotlib.use('QtAgg')
from PyQt6 import QtCore, QtGui, QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


from PyQt6 import uic
from processors import *
from data import *
import os

'''class VerticalNavigationToolbar(NavigationToolbar):
   def __init__(self, canvas, window):
      super().__init__(canvas, window, pack_toolbar=False)

   # override _Button() to re-pack the toolbar button in vertical direction
   def _Button(self, text, image_file, toggle, command):
      b = super()._Button(text, image_file, toggle, command)
      b.pack(side=tk.TOP) # re-pack button in vertical direction
      return b

   # override _Spacer() to create vertical separator
   def _Spacer(self):
      s = tk.Frame(self, width=26, relief=tk.RIDGE, bg="DarkGray", padx=2)
      s.pack(side=tk.TOP, pady=5) # pack in vertical direction
      return s

   # disable showing mouse position in toolbar
   def set_message(self, s):
      pass
'''

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_data = ''
        self.data = Data()
        self.initUi()
        self.Processor = TikhonovProcessor()



        #self.tikhonov_process_button.clicked.connect()
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
        self.plot.axes.plot(t, A)
        self.print_log(path)
        self.print_log("END FUCK YOU")

    def init_plot(self):
        self.plot = MplCanvas(self)
        self.plot.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        self.plot_toolbar = NavigationToolbar(self.plot, self)
        self.plot_layout.addWidget(self.plot_toolbar)
        self.plot_layout.addWidget(self.plot)
        self.plot_x_scale_box.addItems(['Линейно', 'Логарифмически'])
        self.plot_y_scale_box.addItems(['Линейно', 'Логарифмически'])

        self.plot_x_scale_box.textActivated.connect(
            lambda scale:
                self.rescale(self.plot.axes, scale, 0))
        self.plot_y_scale_box.textActivated.connect(
            lambda scale:
                self.rescale(self.plot.axes, scale, 1))

    def init_spectrum(self):
        self.spectrum = MplCanvas(self)
        self.spectrum.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        self.spectrum_toolbar = NavigationToolbar(self.spectrum, self)
        self.spectrum_layout.addWidget(self.spectrum_toolbar)
        self.spectrum_layout.addWidget(self.spectrum)
        self.spectrum_x_scale_box.addItems(['Линейно', 'Логарифмически'])
        self.spectrum_y_scale_box.addItems(['Линейно', 'Логарифмически'])

    def init_log(self):
        self.print_log('Лог запущен')


    def print_log(self, text):
        out = str(text) + '\t' + QtCore.QDateTime.toString(QtCore.QDateTime.currentDateTime()) + '\n'
        self.log_data += out
        self.log.insertPlainText(out)

    def rescale(self, graph, scale, axis):
        print("Масштаб:", scale)
        scales = {'Линейно': 'linear', 'Логарифмически': "log"}
        if axis == 0:
            graph.set_xscale(scales[scale])
        else:
            graph.set_yscale(scales[scale])

    def closeEvent(self, event):
        print('closing')
        with open('Log.txt', 'w') as f:
            print(self.log_data, file=f)
        settings = QtCore.QSettings()
        settings.setValue('geometry', self.saveGeometry())
        settings.setValue('windowState', self.saveState())
        super(MainWindow, self).closeEvent(event)

    def readSettings(self):
        settings = QtCore.QSettings()
        if settings.value("geometry") is not None:
            self.restoreGeometry(settings.value("geometry"))
        if settings.value("windowState") is not None:
            self.restoreState(settings.value("windowState"))


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()