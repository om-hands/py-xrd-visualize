from dataclasses import dataclass
from io import TextIOBase
from pathlib import Path

from matplotlib import ticker
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from scipy.optimize import curve_fit

from visualize import util, visualize
from visualize.visualize import (
    XY,
    ax_conf_pass,
    axis_conf_func,
    fig_conf_func,
    fig_conf_pass,
    fig_func_label,
    multi_ax_func,
    multi_fig_func,
)


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
    ax_func: axis_conf_func = ax_conf_pass,
    fig_conf: fig_conf_func = fig_conf_pass,
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

    def ax_func_xrd(ax: Axes):
        # y axis: log scale
        ax.yaxis.set_major_locator(ticker.LogLocator(10))
        # don't show y value
        ax.yaxis.set_major_formatter(ticker.NullFormatter())

    fig = visualize.arrange_row_1axis_nxy(
        xys=xys,
        legends=legends,
        ax_func=multi_ax_func(
            visualize.arrange_row_default_conf(range_, xscale="linear", yscale="log"),
            ax_func_xrd,
            ax_func,
        ),
        fig_func=multi_fig_func(
            fig_func_label(xlabel, ylabel),
            fig_conf,
        ),
    )

    return fig


def fig_ω_scan_1axis(
    paths: list[TextIOBase | str | Path],
    legends: list[str],
    scantimes_sec: list[float],
    show_range: tuple[float, float],
    ax_func: axis_conf_func = ax_conf_pass,
    fig_conf: fig_conf_func = fig_conf_pass,
    xlabel: str = "ω(deg.)",
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

    def ax_func_xrd(ax: Axes):
        # y axis: log scale
        ax.yaxis.set_major_locator(ticker.LogLocator(10))
        # don't show y value
        ax.yaxis.set_major_formatter(ticker.NullFormatter())

    fig = visualize.arrange_row_1axis_nxy(
        xys=xys,
        legends=legends,
        ax_func=multi_ax_func(
            visualize.arrange_row_default_conf(range_, xscale="linear", yscale="log"),
            ax_func_xrd,
            ax_func,
        ),
        fig_func=multi_fig_func(
            fig_func_label(xlabel, ylabel),
            fig_conf,
        ),
    )

    return fig
