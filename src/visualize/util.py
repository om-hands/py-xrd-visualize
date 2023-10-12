import traceback
import sys
import io
import pathlib


import xrd_xy_parser.xy as xrdxy
from src.visualize.visualize import XY


def read_xy(target_file: io.TextIOBase | str | pathlib.Path) -> XY:
    """
    read file from `target_filename` ,and return x-y data.
    Parameters
    ---
    target_filename:xy-styled file name.

    Return
    ---
    x,y:
        x,y:np.ndarray

    Error
    ---
       If file not found, exit program.
    """
    try:
        return XY(*(xrdxy.read2xy(target_file)))
    except xrdxy.ParseError as e:
        traceback.print_exception(e)
        sys.exit(1)


def slide_XYs_linear(xys: list[XY], slide: float, reverse=False) -> list[XY]:
    if reverse:
        xys.reverse()
    newxy: list[XY] = []

    for i, xy in enumerate(xys):
        y = xy.y + (slide * i)
        newxy.append(XY(xy.x, y))

    return newxy


def slide_XYs_log(xys: list[XY], slide: int, reverse=False) -> list[XY]:
    if reverse:
        xys.reverse()
    newxy: list[XY] = []
    for i, xy in enumerate(xys, 0):
        y = (xy.y + 1) * 10 ** (slide * i)
        newxy.append(XY(xy.x, y))
    return newxy
