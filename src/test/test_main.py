import unittest
from src.visualize import visualize


class Test_visualize(unittest.TestCase):
    def test_arrange_row(self):
        target_files: list[str] = ["src/test/test.xy"]

        xys = list(map(visualize.read_xy, target_files))
        visualize.arrange_row(
            xys=xys,
            range=[38.2, 39],
            sharex=True,
            xlabel=r"$2\theta[°]$",
            ylabel=r"$Intensity[arb. unit]$",
            yscale="log",
        )


if __name__ == "__main__":
    unittest.main()
