from io import TextIOBase
from pathlib import Path
import matplotlib as mpl
from matplotlib.axes import Axes

import matplotlib.pyplot as plt
from py_xrd_visualize import util
from py_xrd_visualize.visualize import (
    Annotater,
    ax_conf_pass,
    ax_default_legends,
    ax_func_horizontal_annotates,
    fig_conf_show,
)

from py_xrd_visualize.xrd import (
    fig_2θ_ω_1axis,
    fig_φ_scan_1axis,
    fig_ω_scan_1axis,
)


def plot_2θ_ω_1axis():
    paths: list[TextIOBase | str | Path] = list(
        map(lambda x: Path("src/test/") / x, ["test.xy"] * 2)
    )

    print(paths)
    fig = fig_2θ_ω_1axis(
        paths,
        [1, 1, 1],
        legends=["test1", "test2", "test3"],
        legend_title="2th omega",
        legend_reverse=True,
        range_=(10, 70),
        # range_=(38.2, 39.0),
        ax_func=ax_func_horizontal_annotates(
            10,
            [
                Annotater(38.5, 0, "38.5,10-5", (0.0, -5)),
                Annotater(38.7, 0, "aaaa"),
            ],
        ),
        fig_conf=fig_conf_show(figratio=(5, 6)),
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

    fig = fig_ω_scan_1axis(
        paths=paths,
        amps=[1400, 35],
        # legends=["test1", "test2noisy"],
        range_=(-4, 4),
        # ax_legends=ax_default_legends(["test1", "test2"]),
        # optimize_func=util.gauss(),
        show_optparam=True,
        fig_conf=fig_conf_show(),
    )
    plt.show()
    # fig.savefig()


def plot_φ_scan_1axis():
    paths: list[TextIOBase | str | Path] = list(
        map(lambda x: Path("src/test/") / x, ["test.xy"] * 2)
    )

    print(paths)

    fig_φ_scan_1axis(
        paths=paths,
        scantimes_sec=[1, 1],
        # legends=["1", ""],
        range_=(0.2, 0.8),
        fig_conf=fig_conf_show(),
        roll_x_deg=0.0,
    )
    # plt.show()

    fig_φ_scan_1axis(
        paths=paths,
        scantimes_sec=[1, 1],
        # legends=["2", ""],
        range_=(0.3, 0.8),
        fig_conf=fig_conf_show(),
        roll_x_deg=0.304,
    )
    fig_φ_scan_1axis(
        paths=paths,
        scantimes_sec=[1, 1],
        # legends=["2", ""],
        range_=(0.3, 0.8),
        fig_conf=fig_conf_show(),
        roll_x_deg=0.311,
    )
    plt.show()
    # fig.savefig()


if __name__ == "__main__":
    mpl.rcParams.update(
        {
            "lines.linewidth": "1.8",
            "font.size": 18,
        }
    )
    # plot_2θ_ω_1axis()
    # plot_ω_scan_1axis()
    plot_φ_scan_1axis()
