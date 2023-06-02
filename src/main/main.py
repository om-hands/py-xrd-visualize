import numpy as np

from src.visualize import visualize


def main():
    target_files: list[str] = ["", ""]
    xys = list(map(visualize.read_file_dummy, target_files))
    visualize.arrange_row(
        xys=xys,
        range=[0.0, 2 * np.pi],
        sharex=True,
        xlabel=r"$2\theta[°]$",
        ylabel=r"$Intensity[arb. unit]$",
        yscale="linear",
    )


if __name__ == "__main__":
    main()
