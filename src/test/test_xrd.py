from io import TextIOBase
from pathlib import Path
from matplotlib.axes import Axes

import matplotlib.pyplot as plt
from visualize import util
from visualize.visualize import (
    Annotater,
    ax_conf_pass,
    ax_default_legends,
    ax_func_horizontal_annotates,
    fig_conf_show,
)

from visualize.xrd import (
    fig_2θ_ω_1axis,
    fig_ω_scan_1axis,
)


def plot_2θ_ω_1axis():
    paths: list[TextIOBase | str | Path] = list(
        map(lambda x: Path(x), ["src/test/test.xy"] * 3)
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
        fig_conf=fig_conf_show(),
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
        legends=["test1", "test2noisy"],
        range_=(-4, 4),
        # ax_legends=ax_default_legends(["test1", "test2"]),
        optimize_func=util.gauss,
        show_optparam=True,
        fig_conf=fig_conf_show(),
    )
    plt.show()
    # fig.savefig()


if __name__ == "__main__":
    plot_2θ_ω_1axis()
    # plot_ω_scan_1axis()
