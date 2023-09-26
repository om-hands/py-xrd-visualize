import traceback
import sys
import io 
import pathlib

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import xrd_xy_parser.xy as xy
from xrd_xy_parser.xy import xrdXY

# import Types
from typing import Tuple, List, Literal
from matplotlib.axes import Axes




def read_xy(target_filename: io.TextIOBase|str|pathlib.Path) -> xrdXY:

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
    range:tuple[float,float],
    
    xlabel: str,
    ylabel: str,
    title: str ,
    save:bool=False,
    ymax: float | None = None,
    ymin:float|None=None,
    major_locator:ticker.Locator=ticker.AutoLocator(),
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
    fig, _axs = plt.subplots(nrows=len(xys), sharex=True, squeeze=False)
    axs = _axs[:, 0]
    
    for _ax, xy in zip(axs, xys): 
        ax:Axes = _ax
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

    plt.grid(False)
    plt.tight_layout()
    plt.show()
    if save:
        fig.savefig(title)
