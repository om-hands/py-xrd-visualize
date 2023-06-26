import traceback
import sys

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import xrd_xy_parser.xy as xy
from xrd_xy_parser.xy import xrdXY

# import Types
from typing import Tuple, List, Literal
from matplotlib.axes import Axes
from io import TextIOBase
from pathlib import Path 


def read_xy(target_filename: TextIOBase|str|Path) -> xrdXY:

    """
    read file from `target_filename` ,and return x-y data.
    Parameters
    ---
    target_filename:xy-styled file name.

    Return
    ---
    x,y:
        x,y:np.ndarray

    Error
    ---
       If file not found, exit program.
    """
    try:
        return xy.read2xy(target_filename)
    except xy.ParseError as e:
        traceback.print_exception(e)
        sys.exit(1)


def read_file_dummy(target_filename: str) -> xrdXY:
    """
    Parameters
    ---
    target_filename:not used.

    Return
    ---
    x,y:
        x:np.ndarray. 0~2π
        y:np.ndarray. sin(x)
    """
    x = np.linspace(0, 2 * np.pi)
    y = np.sin(x)
    return xrdXY(x, y)

def parameter():
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": "Arial",
        }
    )

def arrange_row(
    xys: List[xrdXY],
    range: List[float],
    xlabel: str,
    ylabel: str,
    sharex: bool = True,
    yscale: Literal["linear", "log", "symlog", "logit"] = "symlog",
):

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
    fig, _axs = plt.subplots(nrows=len(xys), sharex=sharex, squeeze=False)
    axs = _axs[:, 0]
    
    for _ax, xy in zip(axs, xys): 
        ax:Axes = _ax
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
        ax.set_yscale(yscale)

        # set ylabel
        ax.set_yticklabels([])

        ax.plot(*xy)

    plt.xlim(range)

    # set labels on the center of figure
    fig.supxlabel(xlabel)
    fig.supylabel(ylabel)

    plt.grid(False)
    plt.tight_layout()
    plt.show()
