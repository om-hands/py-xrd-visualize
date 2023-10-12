import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.figure import Figure
from matplotlib.axes import Axes

# import Types
from typing import Callable, List, Literal, NamedTuple


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


def arrange_row_1axis_nxy(
    xys: List[XY],
    ax_func: Callable[[Axes], None],
    xlabel: str,
    ylabel: str,
) -> Figure:
    """
    Parameters:
        `xys`:xy-styled input data.
        `ax_func`:plot xy on ax.
        `xlabel`,`ylabel`:axis label.


    """
    fig, _ = plt.subplots(nrows=1, sharex=True, squeeze=False)
    ax = fig.axes[0]

    for xy in xys:
        ax.plot(*xy)
        ax_func(ax)

    fig.supxlabel(xlabel)
    fig.supylabel(ylabel)
    return fig


def arrange_row_naxis_nxy(
    xys: List[XY],
    ax_func: Callable[[Axes], None],
    xlabel: str,
    ylabel: str,
) -> Figure:
    """
    Returns a figure with n data plotted on n axes each.
    Parameters:
    ---
        `xys`:xy-styled input data.
        `ax_func`:plot xy on ax.
        `xlabel`,`ylabel`:axis label.
    """
    fig, _ = plt.subplots(nrows=len(xys), sharex=True, squeeze=False)
    axs = fig.axes

    for ax, xy in zip(axs, xys):
        ax.plot(*xy)
        ax_func(ax)

    # set labels on the center of figure
    fig.supxlabel(xlabel)
    fig.supylabel(ylabel)

    return fig


def arrange_row_default_conf(
    range_: tuple[float, float],
    ymax: float | None = None,
    ymin: float | None = None,
    major_locator: ticker.Locator = ticker.AutoLocator(),
    xscale: Literal["linear", "log", "symlog", "logit"] = "linear",
    yscale: Literal["linear", "log", "symlog", "logit"] = "linear",
) -> Callable[[Axes], None]:
    """
    Parameters:
    ---
        `range_`:x-axis range.

        `ymax`,`ymin`:y-axis range,option

        `major_locator`: tick setting

        `xscale`,`yscale`:x-axis,y-axis scale.

    Return
    ---
        `func(ax:Axes)`:plot xy on ax with configuration by this function
    """

    def lambda_(ax: Axes):
        # scale
        ax.set_xscale(xscale)
        ax.set_yscale(yscale)

        # x-limit
        ax.set_xlim(range_)

        # y limit
        if ymin is not None:
            ax.set_ylim(ymin=ymin)

        if ymax is not None:
            ax.set_ylim(ymax=ymax)

        # メモリ自動調整
        ax.xaxis.set_major_locator(major_locator)
        if xscale != "log":
            ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())

        # ticklabel
        # ax.set_xticklabels(np.arange(range[0],range[1]+tick,step=tick))
        ax.set_yticklabels([])

    return lambda_
