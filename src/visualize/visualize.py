import traceback
import sys
from typing import Tuple, List, Literal

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import xrd_xy_parser.xy as xy


def read_xy(target_filename: str) -> Tuple[np.ndarray, np.ndarray]:
    try:
        _, body, _ = xy.readstr(target_filename)
        return body[:, 0], body[:, 1]
    except xy.ParseError as e:
        traceback.print_exception(e)
        sys.exit(1)


def read_file_dummy(target_filename: str) -> Tuple[np.ndarray, np.ndarray]:

    x = np.linspace(0, 2 * np.pi)
    y = np.sin(x)
    return x, y


def arrange_row(
    xys: List[Tuple[np.ndarray, np.ndarray]],
    range: List[float],
    xlabel: str,
    ylabel: str,
    sharex: bool = True,
    yscale: Literal["linear", "log", "symlog", "logit"] = "symlog",
):

    fig, axs = plt.subplots(nrows=len(xys), sharex=sharex)

    # axs is "Axes or array of Axes"
    if isinstance(axs, np.ndarray):
        for ax, xy in zip(axs, xys):  # type: ignore
            ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
            ax.plot(*xy)
    else:
        axs.xaxis.set_minor_locator(ticker.AutoMinorLocator())
        axs.plot(*xys[0])

    plt.xlim(range)

    plt.yscale(yscale)

    # set labels on the center of figure
    fig.supxlabel(xlabel)
    fig.supylabel(ylabel)

    plt.grid(False)
    plt.show()
