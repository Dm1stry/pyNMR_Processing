from PyQt6.QtCore import QObject
import numpy as np


class TikhonovParams:
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

    def setParams(self, params):
        self.T_min = params.T_min
        self.T_max = params.T_max
        self.iterations = params.iterations
        self.alpha = params.alpha
        self.p_size = params.p_size
class Results:
    t = None
    A = None
    pt = None
    p = None

class TikhonovProcessor(QObject):
    def __init__(self):
        super().__init__()
        self.params = TikhonovParams()
        self.results = None

    def setParams(self, params):
        self.params = params

    def Process(self, data):
        p = np.logspace(np.log10(1 / self.params.T_max), np.log10(1 / self.params.T_min), self.params.p_size)
        ts = data.get_data()
        t = ts[0]
        s = ts[1]
        pp, tt = np.meshgrid(p, t)
        K = np.exp(-pp * tt)

        r = self.__regularigation(K, np.zeros(self.params.p_size), s, self.params.alpha, self.params.iterations)

        self.results = Results()
        self.results.t = t
        self.results.A = K @ r
        self.results.pt = 1/p
        self.results.p = r

    def __regularigation(self, K, r, s, alfa, iterations):
        K_t = np.ascontiguousarray(np.transpose(K))

        W = np.ascontiguousarray(np.linalg.inv(K_t @ K + alfa * np.eye(r.size)))
        s = np.ascontiguousarray(s)
        K_t_s = np.ascontiguousarray(K_t @ s)

        for i in range(iterations):
            r = W @ (K_t_s + alfa * r)
            r[r < 0] = 0

        return r

    def getSpectrum(self):
        return self.results.pt, self.results.p

    def getCurve(self):
        return self.results.t, self.results.A
