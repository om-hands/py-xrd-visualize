from dataclasses import dataclass
from io import TextIOBase
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

    # paths: list[Union[str, Path]],


def fig_2θ_ω_1axis(
    paths: list[TextIOBase | str | Path],
    legends: list[str],
    scantimes_sec: list[float],
    range_: tuple[float, float],
    xlabel: str = "2θ(deg.)",
    ylabel: str = "Intensity(arb. unit)",
    slide_exp: float = 2,
    slide_base: float = 1.0,
    reverse_legends: bool = False,
    reverse_xy: bool = False,
) -> Figure:
    xys: list[XY] = []
    for p in paths:
        xys.append(util.read_xy(p))

    # y unit: count per sec
    for xy, st in zip(xys, scantimes_sec):
        xy.y /= st

    if reverse_xy:
        xys.reverse()
    # slide after reverse
    util.slide_XYs_log(xys, slide_exp, slide_base)

    if reverse_legends:
        legends.reverse()

    def ax_func(ax: Axes):
        visualize.arrange_row_default_conf(range_, xscale="linear", yscale="log")(ax)

        # y axis: log scale
        ax.yaxis.set_major_locator(ticker.LogLocator(10))
        # don't show y value
        ax.yaxis.set_major_formatter(ticker.NullFormatter())

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
