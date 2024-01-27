from io import TextIOBase
from pathlib import Path
import matplotlib as mpl

import matplotlib.pyplot as plt
from py_xrd_visualize.XYs import read_xys
from py_xrd_visualize.util import Gauss, Voigt

from py_xrd_visualize.visualize import (
    Annotater,
    ax_func_horizontal_annotates,
    ax_legends,
    ax_plots,
    complete_ax,
    complete_fig,
    fig_conf_show,
)

from py_xrd_visualize.xrd import (
    ax_2θ_ω,
    ax_φ,
    ax_ω,
    fig_any_scan_1axis,
    fig_any_scan_naxis,
    make_fig_1axis,
)


def plot_2θ_ω_1axis():
    paths: list[TextIOBase | str | Path] = list(
        map(lambda x: Path("src/test/") / x, ["test.xy"] * 2)
    )

    print(paths)
    make_fig_1axis(
        ax_2θ_ω(
            paths,
            [1, 1],
            legends=["test1", "test2"],
            legend_title="2th omega",
            legend_reverse=True,
            # range_=(10, 70),
            # range_=(38.2, 39.0),
            ax_funcs=[
                ax_func_horizontal_annotates(
                    10,
                    [
                        Annotater(38.5, 0, "38.5,10-5", (0.0, -5)),
                        Annotater(38.7, 0, "aaaa"),
                    ],
                )
            ],
        ),
        fig_funcs=[fig_conf_show(figratio=(5, 6))],
    )

    plt.show()
    # fig.savefig()


def plot_ω_scan_1axis():
    paths: list[TextIOBase | str | Path] = list(
        map(
            lambda x: Path("src/test/") / x,
            [
                "test_rock_13-19_0.01deg.xy",
                # "test_rock_14.5-16.5_0.01deg.xy",
                "test_rock_13.5-20.5_0.01deg.xy",
            ],
        )
    )

    print(paths)

    make_fig_1axis(
        ax_func=ax_ω(
            paths=paths,
            amps=[1400, 35],
            legends=["test1", "test2noisy"],
            range_=(-4, 4),
            # ax_legends=ax_default_legends(["test1", "test2"]),
            optimizer=Gauss(),
            show_optparam=True,
        ),
        fig_funcs=[fig_conf_show(figratio=(10, 5))],
    )

    make_fig_1axis(
        ax_func=ax_ω(
            paths=paths,
            amps=[1400, 35],
            legends=["test1", "test2noisy"],
            range_=(-4, 4),
            # ax_legends=ax_default_legends(["test1", "test2"]),
            optimizer=Voigt(),
            show_optparam=True,
        ),
        fig_funcs=[fig_conf_show(figratio=(10, 5))],
    )
    plt.show()

    # fig.savefig()


def plot_φ_scan_1axis():
    paths: list[TextIOBase | str | Path] = list(
        map(lambda x: Path("src/test/") / x, ["test.xy"] * 2)
    )

    print(paths)

    # fig_φ_scan_1axis(
    #     paths=paths,
    #     scantimes_sec=[1, 1],
    #     legends=["1", "2"],
    #     range_=(0.2, 0.8),
    #     fig_conf=fig_conf_show(),
    #     roll_x_deg=0.0,
    # )
    make_fig_1axis(
        ax_func=ax_φ(
            paths=paths,
            scantimes_sec=[1, 1],
            legends=["1", "2"],
            range_=(0.2, 0.8),
            roll_x_deg=0.0,
        ),
        fig_funcs=[],
    )
    # plt.show()

    make_fig_1axis(
        ax_func=ax_φ(
            paths=paths,
            scantimes_sec=[1, 1],
            range_=(0.3, 0.8),
            roll_x_deg=0.304,
        ),
        fig_funcs=[],
    )

    make_fig_1axis(
        ax_func=ax_φ(
            paths=paths,
            scantimes_sec=[1, 1],
            # legends=["2", ""],
            range_=(0.3, 0.8),
            roll_x_deg=0.311,
        ),
        fig_funcs=[],
    )

    plt.show()
    # fig.savefig()


def plot_any_scan_1axis():
    paths: list[TextIOBase | str | Path] = list(
        map(
            lambda x: Path("src/test/") / x,
            [
                "test.xy",
                "test_rock_13-19_0.01deg.xy",
                "test_rock_13.5-20.5_0.01deg.xy",
                "test_rock_14.5-16.5_0.01deg.xy",
            ],
        )
    )
    with mpl.rc_context({"font.size": 10}):
        fig_any_scan_1axis(paths)
        fig_any_scan_naxis(paths)
        plt.show()


def complete_test():
    paths: list[TextIOBase | str | Path] = list(
        map(lambda x: Path("src/test/") / x, ["test.xy"] * 2)
    )

    xys = read_xys(paths)
    # xys_2θ_ω_scan(xys, scantimes_sec=[1, 1], slide_exp=2, slide_base=1.0)
    xy1, xy2 = xys
    fig = plt.figure()
    fig.add_subplot(211)
    fig.add_subplot(212)

    cfig = complete_fig(
        ax_funcs=[
            complete_ax(
                ax_plots=ax_plots([xy1]),
                ax_legends=ax_legends(legends=["test1"]),
            ),
            complete_ax(
                ax_plots=ax_plots([xy2]),
                ax_legends=ax_legends(legends=["test2"]),
            ),
        ],
        fig_funcs=[fig_conf_show(figratio=(5, 6))],
    )
    cfig(fig)
    plt.show()

    fig = plt.figure()
    fig.add_subplot(211)
    fig.add_subplot(212)

    cfig(fig)
    plt.show()


if __name__ == "__main__":
    mpl.rcParams.update(
        {
            "lines.linewidth": "1.8",
            "font.size": 18,
        }
    )
    plot_2θ_ω_1axis()
    plot_ω_scan_1axis()
    plot_φ_scan_1axis()
    plot_any_scan_1axis()
    complete_test()
