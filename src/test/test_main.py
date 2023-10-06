import traceback
from typing import Any, Callable

import numpy as np
import io
import sys

from src.visualize import visualize, util
import matplotlib.pyplot as plt

# from matplotlib.figure import Figure

from matplotlib.ticker import MultipleLocator


def generate_xy(range_: tuple[float, float], f: Callable[[Any], Any]):
    x = np.linspace(*range_)
    y = f(x)
    return visualize.XY(x, y)


def Test_arrange_dummy_sine():
    range_ = (0, 2 * np.pi)
    xys = [generate_xy(range_, np.sin)]

    visualize.arrange_row(
        xys=xys,
        range=range_,
        xlabel=r"$2\theta[°]$",
        ylabel=r"$Intensity[arb. unit]$",
        yscale="linear",
    )

    plt.suptitle("dummysine")
    plt.show()


def test_arrange_dummy_nth(n: int):
    range_ = (0.0, 2 * np.pi)
    xy = generate_xy(range_, np.sin)
    xys = [xy] * n

    axs = visualize.arrange_row(
        xys=xys,
        range=range_,
        xlabel=r"$2\theta[°]$",
        ylabel=r"$Intensity[arb. unit]$",
        yscale="linear",
    ).axes
    for i, ax in enumerate(axs):
        ax.set_title(str(i) + "th dummy")

    plt.suptitle("dummysine*n")
    plt.show()


def Test_arrange_dummy_nth():
    test_arrange_dummy_nth(5)


def Test_arrange_rawdata():
    xys = list(map(util.read_xy, ["src/test/test.xy"]))
    ax = visualize.arrange_row(
        xys=xys,
        range=(38.2, 39.0),
        xlabel=r"$2\theta[°]$",
        ylabel=r"$Intensity[arb. unit]$",
        ymax=50,
        yscale="log",
    ).axes[0]

    ax.text(38.5, 10, "pointing", horizontalalignment="center", rotation="vertical")

    plt.suptitle("Test_arrange_rawdata")
    plt.grid(True)
    plt.show()


def test_arrange_rawdata_nth(n: int):
    xys = list(map(util.read_xy, ["src/test/test.xy"] * n))
    visualize.arrange_row(
        xys=xys,
        range=(38.2, 39),
        xlabel=r"$2\theta[°]$",
        ylabel=r"$Intensity[arb. unit]$",
        ymax=50,
        yscale="log",
    )
    plt.suptitle(f"Test_arrange_rawdata_{n}th")
    plt.show()


def Test_arrange_rawdata2():
    data = """30.0000	15.0000
30.0100	13.0000
30.0200	19.0000
30.0300	10.0000
30.0400	15.0000
30.0500	16.0000
30.0600	14.0000
30.0700	24.0000
30.0800	8.0000
30.0900	15.0000
30.1000	9.0000
30.1100	11.0000
30.1200	12.0000
30.1300	8.0000
30.1400	19.0000
30.1500	12.0000
30.1600	10.0000
30.1700	12.0000
30.1800	13.0000
30.1900	24.0000
30.2000	17.0000
30.2100	18.0000
30.2200	13.0000
30.2300	18.0000
30.2400	13.0000
30.2500	17.0000
30.2600	16.0000
30.2700	12.0000
30.2800	18.0000
30.2900	15.0000
30.3000	15.0000
30.3100	18.0000
30.3200	16.0000
30.3300	19.0000
30.3400	19.0000
30.3500	15.0000
30.3600	19.0000
30.3700	10.0000
30.3800	15.0000
30.3900	15.0000
30.4000	14.0000
30.4100	17.0000
30.4200	9.0000
30.4300	10.0000
30.4400	15.0000
30.4500	17.0000
30.4600	12.0000
30.4700	14.0000
30.4800	17.0000
30.4900	13.0000
30.5000	20.0000"""
    data = io.StringIO(data)
    xys = list(map(util.read_xy, [data]))
    visualize.arrange_row(
        xys=xys,
        range=(30.0, 30.5),
        xlabel=r"$2\theta[°]$",
        ylabel=r"$Intensity[arb. unit]$",
        ymax=50,
        ymin=1,
        major_locator=MultipleLocator(0.2),
        yscale="log",
    )
    plt.suptitle("Test_arrange_rawdata2")
    plt.show()


def Test_arrange_rawdata_nth():
    test_arrange_rawdata_nth(5)


def main():
    visualize.parameter()

    # グローバルに定義されている関数のうち，"Test"で始まる関数を呼び出す
    # やりにくいけど見た目の設定をテストするのでunittest等が使えなかったのでしょうがない．
    for k_attrname, v_attr_obj in globals().items():
        if k_attrname.startswith("Test") and callable(v_attr_obj):
            try:
                print("test:", k_attrname, file=sys.stderr)
                v_attr_obj()
            except TypeError as e:
                print(
                    "{k_attrname} start with 'Test' but need argument", file=sys.stderr
                )
                traceback.print_exception(e)


if __name__ == "__main__":
    main()
