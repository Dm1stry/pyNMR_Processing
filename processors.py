from abc import ABC, abstractmethod, abstractproperty
import numpy as np


class Processor(ABC):
    @abstractmethod
    def Process(self, T_min, T_max, data, iterations=1000):
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

    def Process(self, T_min, T_max, data, iterations=1000):
        self.__alfa = 20
        p_size = 10000
        self.__p = np.logspace(np.log10(1 / T_max), np.log10(1 / T_min), p_size)
        self.__t = data[:, 0]
        self.__s = data[:, 1]
        pp, tt = np.meshgrid(self.__p, self.__t)
        self.__K = np.exp(-pp * tt)
        K_t = np.transpose(self.__K)
        self.__r = np.zeros_like(self.__p)

        W = np.linalg.inv(K_t @ self.__K + self.__alfa * np.eye(self.__p.size))
        K_t_s = K_t @ self.__s
        for i in range(iterations):
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



