import traceback
import sys
import io
import pathlib

import numpy as np

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


def read_file_dummy(target_filename: str) -> XY:
    """
    Parameters
    ---
    target_filename:not used.

    Return
    ---
    x,y:
        x:np.ndarray. 0~2π
        y:np.ndarray. sin(x)
    """
    x = np.linspace(0, 2 * np.pi)
    y = np.sin(x)
    return XY(x, y)
