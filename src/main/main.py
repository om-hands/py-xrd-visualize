import traceback
import sys
from typing import Tuple, List, Literal

import numpy as np
import matplotlib.pyplot as plt
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

    if isinstance(axs, np.ndarray):
        for ax, xy in zip(axs, xys):  # type: ignore
            ax.plot(*xy)  # set data
    else:
        axs.plot(*xys[0])  # set data

    plt.yscale(yscale)
    plt.xlim(range)

    fig.supxlabel(xlabel)
    fig.supylabel(ylabel)

    plt.grid(False)
    plt.show()


def main():
    target_files: list[str] = ["", ""]
    xys = list(map(read_file_dummy, target_files))
    arrange_row(
        xys=xys,
        range=[0.0, 2 * np.pi],
        sharex=True,
        xlabel=r"$2\theta[°]$",
        ylabel=r"$Intensity[arb. unit]$",
        yscale="linear",
    )


if __name__ == "__main__":
    main()
