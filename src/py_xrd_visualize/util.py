import numpy as np
import scipy


def gauss(x, amp, center, sigma):
    """
    parameter order:
        [amp, center, sigma]
    """
    return amp * np.exp(-((x - center) ** 2) / (2 * sigma**2))


def gauss_const_bg(x, amp, center, sigma, const_):
    """
    parameter order:
        [amp, center, sigma]
        const_:constant background
    """
    return amp * np.exp(-((x - center) ** 2) / (2 * sigma**2)) + const_


def __voigt(x, amp, center, gw, lw):
    """
    https://qiita.com/yamadasuzaku/items/4fccdc90fa13746af1e1

    Parameters:
        `amp` : amplitude
        `center `: center of Lorentzian line
        `gw` : sigma of the gaussian
        `lw` : FWHM of Lorentzian

    """

    z = (x - center + 1j * lw) / (gw * np.sqrt(2.0))
    w = scipy.special.wofz(z)
    y = amp * (w.real) / (gw * np.sqrt(2.0 * np.pi))
    return y
