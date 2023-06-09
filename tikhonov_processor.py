from PyQt6.QtCore import QObject
import numpy as np
from scipy.signal import argrelextrema


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
        W_K_t_s = W @ (K_t @ s)
        W_alfa = np.ascontiguousarray(W * alfa)

        for i in range(iterations):
            r = W_K_t_s + W_alfa @ r
            r[r < 0] = 0

        return r

    def getSpectrum(self):
        return self.results.pt, self.results.p

    def getCurve(self):
        return self.results.t, self.results.A

    def getComponents(self):
        complete_S = np.trapz(self.results.p)
        peaks = argrelextrema(self.results.p, np.greater)[0]
        #mins = argrelextrema(self.results.p, np.greater)
        components = []
        for peak in peaks:
            components.append((self.results.pt[peak], self._find_peak_S(peak)/complete_S))
        return components

    def _find_peak_S(self, peak_index):
        current_index_up = peak_index
        current_index_down = peak_index
        while(self.results.p[current_index_up] != 0):
            if current_index_up == len(self.results.p) - 1:
                break
            current_index_up += 1
        while (self.results.p[current_index_down] != 0):
            if current_index_down == 0:
                break
            current_index_down -= 1
        return np.trapz(self.results.p[current_index_down:current_index_up])
