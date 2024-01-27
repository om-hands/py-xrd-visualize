import numpy as np
from py_xrd_visualize.XYs import XY


def range_from_xys_widest(xys: list[XY]) -> tuple[float, float]:
    range_ = (np.inf, -np.inf)
    for xy in xys:
        range_ = (min(range_[0], xy.x.min()), max(range_[1], xy.x.max()))
    print(range_)
    return range_
