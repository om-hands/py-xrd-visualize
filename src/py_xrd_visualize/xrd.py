from dataclasses import dataclass
from io import TextIOBase
from pathlib import Path

from matplotlib import ticker
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import numpy as np
from py_xrd_visualize.XYs import (
    XY,
    normalize_y_cps,
    read_xys,
    reorder_x,
    roll_x,
    shift_x_center_rough,
    shift_x0,
    slide_y_log,
)


from py_xrd_visualize.util import (
    Optimizer,
    Gauss,
)
from py_xrd_visualize.visualize import (
    arrange_row_1axis_nxy,
    ax_conf_default,
    ax_conf_pass,
    ax_default_legends,
    axis_conf_func,
    fig_conf_func,
    fig_conf_pass,
    fig_conf_show,
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


def ax_format_y_log_arbunits(ax: Axes):
    # y axis: log scale
    ax.yaxis.set_major_locator(ticker.LogLocator(10))

    # show minor ticks
    ax.yaxis.set_minor_locator(
        ticker.LogLocator(numticks=10, subs=(np.arange(1, 10) * 0.1).tolist())
    )
    # don't show y value
    ax.yaxis.set_major_formatter(ticker.NullFormatter())
    ax.yaxis.set_minor_formatter(ticker.NullFormatter())


def xys_2θ_ω_scan(
    xys: list[XY], scantimes_sec: list[float], slide_exp: float, slide_base: float
):
    normalize_y_cps(xys, scantimes_sec)
    slide_y_log(xys, slide_exp, slide_base)


def fig_2θ_ω_1axis(
    paths: list[TextIOBase | str | Path],
    scantimes_sec: list[float],
    range_: tuple[float, float],
    ax_func: axis_conf_func = ax_conf_pass,
    fig_conf: fig_conf_func = fig_conf_pass,
    xlabel: str = "2θ(deg.)",
    ylabel: str = "Intensity(arb. unit)",
    legends: list[str] | None = None,
    legend_title: str = "",
    legend_reverse: bool = False,
    slide_exp: float = 2,
    slide_base: float = 1.0,
) -> Figure:
    xys = read_xys(paths)
    xys_2θ_ω_scan(xys, scantimes_sec, slide_exp, slide_base)

    fig = arrange_row_1axis_nxy(
        xys=xys,
        ax_legends=ax_default_legends(legends, legend_title, legend_reverse),
        ax_func=multi_ax_func(
            ax_conf_default(range_, xscale="linear", yscale="log"),
            ax_format_y_log_arbunits,
            ax_func,
        ),
        fig_func=multi_fig_func(
            fig_func_label(xlabel, ylabel),
            fig_conf_show(),
            fig_conf,
        ),
    )

    return fig


def xys_ω_scan(
    xys: list[XY], amps: list[float], optimizers: list[Optimizer]
) -> list[list[float]]:
    shift_x_center_rough(xys)

    pinits = []
    # init param ; center is ~0 by shift_x_center_rough
    for optimizer, amp in zip(optimizers, amps):
        pinits.append(optimizer.initparam(amp, 0, 1))

    # fitting
    popts = []
    for xy, optimizer, pinit in zip(xys, optimizers, pinits):
        popt, _ = optimizer.fitting(xy, pinit)
        popts.append(popt)

    # centering and normalize
    for xy, optimizer, popt in zip(xys, optimizers, popts):
        center = optimizer.center(popt)
        xy.x -= center
        xy.y /= optimizer.func(center, *popt)

    return popts


def fig_ω_scan_1axis(
    paths: list[TextIOBase | str | Path],
    amps: list[float],
    range_: tuple[float, float],
    ax_func: axis_conf_func = ax_conf_pass,
    fig_conf: fig_conf_func = fig_conf_pass,
    xlabel: str = "ω(deg.)",
    ylabel: str = "Intensity(arb. unit)",
    legends: list[str] | None = None,
    legend_title: str = "",
    legend_reverse: bool = False,
    optimizer: Optimizer = Gauss(),
    show_optparam: bool = False,
) -> Figure:
    xys = read_xys(paths)

    optimizers = [(optimizer) for _ in amps]
    popts = xys_ω_scan(xys, amps, optimizers)

    def ax_func_format(ax: Axes):
        # show range includes amp(=1.0),
        ax.set_ylim(ymin=0, ymax=1.5)

        # y axis: linear scale
        ax.yaxis.set_major_locator(ticker.LinearLocator())
        ax.yaxis.set_minor_locator(ticker.LinearLocator(21))

        # don't show y value
        ax.yaxis.set_major_formatter(ticker.NullFormatter())

    def ax_func_opt(legends: list[str] | None):
        if not show_optparam:
            return ax_conf_pass

        if legends is None:
            legends = [f"{i}" for i, _ in enumerate(popts)]

        ann_texts = []

        def ax_func(ax: Axes):
            for popt, legend, optimizer in zip(popts, legends, optimizers):
                ann_text = f"{legend}:{optimizer.toString(popt)}"
                ann_texts.append(ann_text)

                x = np.linspace(*range_)
                # plot ideal func (center=0)
                popt_center = [popt[0], 0, *popt[2:]]
                y = np.vectorize(optimizer.func)(x, *popt_center)

                # normalize y to 1 on x=0
                ymax = np.max(y)
                y /= ymax

                # plot fit curve
                ax.plot(x, y)

                hwhm = optimizer.fwhm(popt) / 2
                # 1.8 is arbitrary
                xy = (hwhm, optimizer.func(hwhm, *popt_center) / ymax * 1.8)
                ax.annotate(
                    ann_text,
                    xy=xy,
                    horizontalalignment="left",
                    verticalalignment="baseline",
                )
            print("optimized param")
            for ann_text in ann_texts:
                print(ann_text)

        return ax_func

    fig = arrange_row_1axis_nxy(
        xys=xys,
        ax_legends=ax_default_legends(legends, legend_title, legend_reverse),
        ax_func=multi_ax_func(
            ax_conf_default(range_, xscale="linear", yscale="linear"),
            ax_func_opt(legends),
            ax_func_format,
            ax_func,
        ),
        fig_func=multi_fig_func(
            fig_func_label(xlabel, ylabel),
            fig_conf_show(),
            fig_conf,
        ),
    )

    return fig


def xys_φ_scan(
    xys: list[XY],
    scantimes_sec: list[float],
    roll_x_deg: float,
    slide_exp: float,
    slide_base: float,
):
    normalize_y_cps(xys, scantimes_sec)
    shift_x0(xys)
    roll_x(xys, roll_x_deg)
    reorder_x(xys)
    slide_y_log(xys, slide_exp, slide_base)


def fig_φ_scan_1axis(
    paths: list[TextIOBase | str | Path],
    scantimes_sec: list[float],
    range_: tuple[float, float] = (0, 360),
    ax_func: axis_conf_func = ax_conf_pass,
    fig_conf: fig_conf_func = fig_conf_pass,
    xlabel: str = "φ(deg.)",
    ylabel: str = "Intensity(arb. unit)",
    legends: list[str] | None = None,
    legend_title: str = "",
    legend_reverse: bool = False,
    roll_x_deg: float = 0,
    slide_exp: float = 2,
    slide_base: float = 1.0,
) -> Figure:
    xys = read_xys(paths)

    xys_φ_scan(xys, scantimes_sec, roll_x_deg, slide_exp, slide_base)

    fig = arrange_row_1axis_nxy(
        xys=xys,
        ax_legends=ax_default_legends(legends, legend_title, legend_reverse),
        ax_func=multi_ax_func(
            ax_conf_default(range_, xscale="linear", yscale="log"),
            ax_format_y_log_arbunits,
            ax_func,
        ),
        fig_func=multi_fig_func(
            fig_func_label(xlabel, ylabel),
            fig_conf_show(),
            fig_conf,
        ),
    )

    return fig
