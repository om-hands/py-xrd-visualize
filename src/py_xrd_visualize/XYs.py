import traceback
import sys
import io
import pathlib
from dataclasses import dataclass
from typing import Sequence

import numpy as np

import xrd_xy_parser.xy as xrdxy


@dataclass
class XY:
    x: np.ndarray
    y: np.ndarray

    def to_tuple(self) -> tuple[np.ndarray, np.ndarray]:
        return (self.x, self.y)


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


def read_xys(target_files: list[io.TextIOBase | str | pathlib.Path]) -> list[XY]:
    xys: list[XY] = []
    for p in target_files:
        xys.append(read_xy(p))
    return xys


def slide_y_linear(xys: list[XY], slide: float):
    for i, xy in enumerate(xys):
        xy.y += slide * i


def slide_y_log(xys: list[XY], slide: float, base: float = 1.0):
    for i, xy in enumerate(xys):
        xy.y = (xy.y + 1) * base * 10 ** (slide * i)


def normalize_y_cps(xys: Sequence[XY], scantimes_sec: Sequence[float]):
    """set y unit cps (count per sec)"""
    for xy, st in zip(xys, scantimes_sec):
        xy.y /= st


# shift x-axis to center roughly
def shift_x_center_rough(xys: Sequence[XY]):
    for xy in xys:
        x = xy.x
        x -= (x[0] + x[-1]) / 2.0


def shift_x0(xys: Sequence[XY]):
    """shift x axis to 0"""
    for xy in xys:
        x0 = xy.x.min()
        xy.x -= x0


def roll_x(xys: Sequence[XY], roll_x_deg: float):
    """roll x axis. call on xy.x.min is 0 ,i.e. call after `shift_x0`"""
    for xy in xys:
        xmax = xy.x.max()
        # roll_x_deg = [0,xmax)
        roll_x_deg %= xmax
        xy.x += roll_x_deg
        xy.x[xy.x > xmax] -= xmax


def reorder_x(xys: Sequence[XY]):
    """reorder array"""
    for xy in xys:
        idx = xy.x.argmin()
        # sort xy and reserve x to y mapping
        xy.x = np.roll(xy.x, -idx)
        xy.y = np.roll(xy.y, -idx)