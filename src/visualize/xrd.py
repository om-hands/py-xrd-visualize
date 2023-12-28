from dataclasses import dataclass
from pathlib import Path

from matplotlib import ticker
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from src.visualize import util, visualize
from src.visualize.visualize import XY


@dataclass()
class Scaned:
    path: Path
    legend: str
    scantime_s: float


def fig_2θ_ω_1axis(
    paths: list[Path],
    legends: list[str],
    scantimes_sec: list[float],
    xlabel: str,
    ylabel: str,
    range_: tuple[float, float],
    slide: float = 1e3,
    slide_base: float = 1.0,
    reverse_legends: bool = False,
    reverse_xy: bool = False,
):
    xys: list[XY] = []
    for p in paths:
        xys.append(util.read_xy(p))

    # y unit: count per sec
    for xy, st in zip(xys, scantimes_sec):
        xy.y /= st

    if reverse_xy:
        xys.reverse()
    # slide after reverse
    util.slide_XYs_log(xys, slide, slide_base)

    if reverse_legends:
        legends.reverse()

    def ax_func(ax: Axes):
        visualize.arrange_row_default_conf(range_, xscale="linear", yscale="log")(ax)

        ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
        ax.set_yticklabels([])

    return visualize.arrange_row_1axis_nxy(
        xys=xys,
        legends=legends,
        ax_func=ax_func,
        xlabel=xlabel,
        ylabel=ylabel,
    )


def fig_conf(
    fig: Figure,
    dpi: float | None = None,
    figratio: tuple[float, float] | None = None,
    pad: float = 0.4,
):
    if dpi is not None:
        fig.set_dpi(dpi)

    if figratio is not None:
        fig.set_size_inches(*figratio)

    fig.tight_layout(pad=pad)
    return fig

    # visualize.arrange_row_1axis_nxy(xys=)
