from io import TextIOBase
from pathlib import Path

import matplotlib.pyplot as plt
from src.visualize.visualize import fig_conf_show

from src.visualize.xrd import fig_2θ_ω_1axis


def plot_2θ_ω_1axis():
    paths: list[TextIOBase | str | Path] = list(
        map(lambda x: Path(x), ["src/test/test.xy"] * 3)
    )

    print(paths)
    fig = fig_2θ_ω_1axis(
        paths,
        ["test1", "test2", "test3"],
        [1, 1, 1],
        range_=(38.2, 39.0),
        fig_conf=fig_conf_show(),
    )

    # fig_conf(fig, dpi=100, figratio=(4, 4))

    plt.show()
    # fig.savefig()


if __name__ == "__main__":
    plot_2θ_ω_1axis()
