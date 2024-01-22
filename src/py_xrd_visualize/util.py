from abc import ABC, abstractmethod
from typing import Sequence
import numpy as np
from py_xrd_visualize.XYs import XY
import scipy
from scipy.optimize import curve_fit


class Optimizer(ABC):
    """
    Fitting class
    description:
        reserve optimized parameters and initial parameters.
        common for amp,center
        each subclass implement each initial parameters,`fitfunc` and `hwhm` method.
    """

    @staticmethod
    @abstractmethod
    def initparam(amp, center, width) -> list[float]:
        pass

    @staticmethod
    @abstractmethod
    def func(x, amp, center, widthlike, *args) -> float:
        """return fitting function"""
        pass

    @staticmethod
    @abstractmethod
    def hwhm(popt: Sequence[float]) -> float:
        pass

    @staticmethod
    @abstractmethod
    def center(popt: Sequence[float]) -> float:
        pass

    def fitting(self, xy: XY, pinit: Sequence[float]) -> tuple[float, float]:
        popt, pcov = curve_fit(self.func, xdata=xy.x, ydata=xy.y, p0=pinit)
        return popt, pcov


class Gauss(Optimizer):
    @staticmethod
    def initparam(amp, center, width) -> list[float]:
        sigma = width
        bg_c = 0
        return [amp, center, sigma, bg_c]

    @staticmethod
    def func(x, amp, center, sigma, bg_c) -> float:
        """
        parameter order:
            [amp, center, sigma]
            `bg_c`: constant background
        """
        return amp * np.exp(-((x - center) ** 2) / (2 * sigma**2)) + bg_c

    @staticmethod
    def hwhm(popt: Sequence[float]) -> float:
        sigma = popt[2]
        return sigma * 2.355

    @staticmethod
    def center(popt: Sequence[float]) -> float:
        return popt[1]


class Voigt(Optimizer):
    @staticmethod
    def initparam(amp, center, width) -> list[float]:
        lw = width
        gw = 1
        bg_c = 0
        return [amp, center, lw, gw, bg_c]

    @staticmethod
    def func(x, amp, center, lw, gw, bg_c) -> float:
        """
        https://qiita.com/yamadasuzaku/items/4fccdc90fa13746af1e1
        Parameters:
            `amp` : amplitude
            `center `: center of Lorentzian line
            `lw` : HWHM of Lorentzian
            `gw` : sigma of the gaussian
            `bg_c`: constant background
        """
        z = (x - center + 1j * lw) / (gw * np.sqrt(2.0))
        w = scipy.special.wofz(z)
        y = amp * (w.real) / (gw * np.sqrt(2.0 * np.pi)) + bg_c
        return y

    @staticmethod
    def hwhm(popt: Sequence[float]) -> float:
        _, _, lw, gw = popt
        """https://en.wikipedia.org/wiki/Voigt_profile"""
        fl = 2 * lw
        fg = 2.354820 * gw
        return 0.5346 * fl + np.sqrt(0.2166 * fl**2 + fg**2)

    @staticmethod
    def center(popt: Sequence[float]) -> float:
        return popt[1]
