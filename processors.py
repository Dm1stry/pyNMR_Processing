from abc import ABC, abstractmethod, abstractproperty
import numpy as np


class Processor(ABC):

    @abstractmethod
    def setParams(self, params):
        pass

    @abstractmethod
    def Process(self):
        pass

    @abstractmethod
    def getSpectrum(self):
        pass

    @abstractmethod
    def getCurve(self):
        pass


class TikhonovProcessor(Processor):

    def __init__(self):
        self.__K = None
        self.__s = None
        self.__r = None
        self.__t = None
        self.__p = None
        self.__alfa = 0

        self.T_min = 0
        self.T_max = 10e6
        self.data = None
        self.iterations = 1000

    def setParams(self, params):
        self.T_min = params.T_min
        self.T_max = params.T_max
        self.data = params.data
        self.iterations = params.iterations

    def Process(self):
        self.__alfa = 20
        p_size = 10000
        self.__p = np.logspace(np.log10(1 / self.T_max), np.log10(1 / self.T_min), p_size)
        self.__t = self.data[:, 0]
        self.__s = self.data[:, 1]
        pp, tt = np.meshgrid(self.__p, self.__t)
        self.__K = np.exp(-pp * tt)
        K_t = np.transpose(self.__K)
        self.__r = np.zeros_like(self.__p)

        W = np.linalg.inv(K_t @ self.__K + self.__alfa * np.eye(self.__p.size))
        K_t_s = K_t @ self.__s
        for i in range(self.iterations):
            self.__r = W @ (K_t_s + self.__alfa * self.__r)
            self.__r[self.__r < 0] = 0

    def getSpectrum(self):
        return [1/self.__p, self.__r]

    def getCurve(self):
        return [self.__t, self.__K @ self.__r]

class EntropyProcessor(Processor):
    def __init__(self):
        pass

    #def Process(self):

    #def Process(self, T_min, T_max, data, iterations=1000):



