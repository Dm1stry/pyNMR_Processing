from PyQt6.QtCore import QObject


class Params:
    alpha = 200
    iterations = 1000
    T_min = 1e-9
    T_max = 1e9
    p_size = 1000

    def __init__(self, T_min=1e-9, T_max=1e9, iterations=1000, alpha=200, p_size=1000):
        self.T_min = T_min
        self.T_max = T_max
        self.iterations = iterations
        self.alpha = alpha
        self.p_size = p_size


class TikhonovProcessor(QObject):
    def __init__(self):
        super().__init__()
        self.params = None

    def setParams(self, params):
        self.params = params

    def Process(self, data):
        pass

    def getSpectrum(self):
        pass

    def getCurve(self):
        pass
