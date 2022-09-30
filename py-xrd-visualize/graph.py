# from matplotlib.axes import Axes
# from matplotlib.axis import Axis
import matplotlib.pyplot as plt

# import matplotlib.figure as
# from matplotlib.figure import Figure
from xrd_xy_parser import xy
import numpy as np


class AxisHolder:
    "limやらのパラメータは受けるがxylistは持たない"

    def __init__(self) -> None:

        # self.fig: Figure
        # self.axs: Axes | list[Axes]
        # self.fig, self.axs = plt.subplots(len(graphlist))
        self.fig, self.axs = plt.subplots()
        # self.axs.set_xticks
        # legend
        # y offset list

    def setXlim(self, set=False, small=0.0, large=180.0):
        pass

    def setYOffset(bool):
        #  10**(3*i)
        pass

    def showlegend(bool):
        pass

    def setlegend():
        # optine
        pass

    # set
    def setReverse(bool):
        pass

    def saveimage():
        pass


axixholder = AxisHolder()


def main():
    xylist = [0]

    # setXlim(flag, xylist)

    pass


if __name__ == "__main__":
    main()
