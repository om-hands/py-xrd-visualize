import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.figure import Figure


# import Types
from typing import List, Literal, NamedTuple
from matplotlib.axes import Axes


class XY(NamedTuple):
    x: np.ndarray
    y: np.ndarray


def parameter():
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": "Arial",
        }
    )


def arrange_row(
    xys: List[XY],
    range: tuple[float, float],
    xlabel: str,
    ylabel: str,
    ymax: float | None = None,
    ymin: float | None = None,
    major_locator: ticker.Locator = ticker.AutoLocator(),
    yscale: Literal["linear", "log", "symlog", "logit"] = "symlog",
) -> Figure:
    """
    `arrange_row` displays a graph of the list of data `xys`.

    Parameters:
    ---
        `xys`:xy-styled input data.

        `range`:x-axis range.

        `xlabel`,`ylabel`:label.

        `sharex`:is share x-axis.

        `yscale`:y-axis scale.
    """
    # axs is "Axes or array of Axes".
    # if squeeze=False,axs is always array of Axes
    fig, _axs = plt.subplots(nrows=len(xys), sharex=True, squeeze=False)
    axs = _axs[:, 0]

    for _ax, xy in zip(axs, xys):
        ax: Axes = _ax
        ax.plot(*xy)

        # scale
        ax.set_yscale(yscale)

        # limit
        ax.set_xlim(range)
        if ymin is not None:
            ax.set_ylim(ymin=ymin)

        if ymax is not None:
            ax.set_ylim(ymax=ymax)

        # メモリ自動調整
        ax.xaxis.set_major_locator(major_locator)
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())

        # ticklabel
        # ax.set_xticklabels(np.arange(range[0],range[1]+tick,step=tick))
        ax.set_yticklabels([])

    # set labels on the center of figure
    fig.supxlabel(xlabel)
    fig.supylabel(ylabel)

    return fig
