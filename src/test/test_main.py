import traceback
import numpy as np
from src.visualize import visualize
from typing import Callable, Tuple, List, Literal


def Test_arrange_dummy():
    xys = list(map(visualize.read_file_dummy, ["dummysine"]))
    visualize.arrange_row(
        xys=xys,
        range=[0.0, 2 * np.pi],
        sharex=True,
        xlabel=r"$2\theta[°]$",
        ylabel=r"$Intensity[arb. unit]$",
        yscale="linear",
    )


def test_arrange_dummy_nth(n: int):
    xys = list(map(visualize.read_file_dummy, ["dummysine"] * n))
    visualize.arrange_row(
        xys=xys,
        range=[0.0, 2 * np.pi],
        sharex=True,
        xlabel=r"$2\theta[°]$",
        ylabel=r"$Intensity[arb. unit]$",
        yscale="linear",
    )


def Test_arrange_dummy_nth():
    test_arrange_dummy_nth(5)


def Test_arrange_rawdata():

    xys = list(map(visualize.read_xy, ["src/test/test.xy"]))
    visualize.arrange_row(
        xys=xys,
        range=[38.2, 39],
        sharex=True,
        xlabel=r"$2\theta[°]$",
        ylabel=r"$Intensity[arb. unit]$",
        yscale="log",
    )


def test_arrange_rawdata_nth(n: int):

    xys = list(map(visualize.read_xy, ["src/test/test.xy"] * n))
    visualize.arrange_row(
        xys=xys,
        range=[38.2, 39],
        sharex=True,
        xlabel=r"$2\theta[°]$",
        ylabel=r"$Intensity[arb. unit]$",
        yscale="log",
    )


def Test_arrange_rawdata_nth():
    test_arrange_rawdata_nth(5)


def main():

    for k_attrname, v_attr_obj in globals().items():
        if k_attrname.startswith("Test") and callable(v_attr_obj):
            try:
                v_attr_obj()
            except TypeError as e:
                print("{k_attrname} start with 'Test' but need argument")
                traceback.print_exception(e)


if __name__ == "__main__":
    main()
