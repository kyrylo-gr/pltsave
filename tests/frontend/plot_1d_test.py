import matplotlib.pyplot as plt

from ..test_utils import BaseTest, COLORS, get_data


class ClassicalPlotsTest(BaseTest):
    def test_data_with_fit(self):
        fig, ax = plt.subplots(1, 1)

        ax.plot(
            *get_data(),
            markerfacecolor="none",
            markeredgecolor=COLORS[0],
            marker="h",
            linestyle="none",
            label="data"
        )
        ax.plot(*get_data(), color=COLORS[1], linewidth=2, alpha=0.3, label="fit")

        ax.legend()
        self.assertConversionRight(fig)

    def test_unusual_grid(self):
        fig = plt.figure()
        ax1, ax2, ax3 = plt.subplot(221), plt.subplot(223), plt.subplot(122)

        ax1.plot(*get_data(), color=COLORS[0], linestyle="none", marker="x", label="data")
        ax1.plot(*get_data(), color=COLORS[1], label="fit")
        ax1.legend()

        ax2.plot(*get_data(), linestyle="none", marker="x", label="data")
        ax2.plot(*get_data(), label="fit")

        ax3.plot(*get_data(), linestyle="none", marker="x", label="data")

        ax1.set(title="Ampliture", ylabel="Ampliture (mV)")
        ax2.set(title="Phase", ylabel="Phase (deg)", xlabel="Frequency (Hz)")
        ax3.set(title="Phase", ylabel="Phase (deg)", xlabel="Frequency (Hz)")
        ax3.legend(loc=5)

        fig.tight_layout()

        self.assertConversionRight(fig)

    def test_annotation_lines(self):
        fig, ax = plt.subplots(1, 1)

        ax.plot(*get_data(), color=COLORS[1], linestyle="none", marker="x", label="data")
        ax.plot(*get_data(), label="fit")

        ax.axvline(1, color="k", linestyle="--", label="vertical line")

        ax.axhline(0.5, color="k", linestyle="--", label="horizontal line")

        ax.vlines([2, 3], -0.5, 0.5, color=COLORS[2], label="half vertical lines")
        ax.hlines([0, -0.5], 1, 3, color=COLORS[3], label="half horizontal lines")
        ax.legend()

        fig.tight_layout()

        self.assertConversionRight(fig)

    def test_annotation_text(self):
        fig, ax = plt.subplots(1, 1)

        ax.plot(*get_data(), color=COLORS[1], linestyle="none", marker="x", label="data")
        ax.plot(*get_data(), label="fit")

        ax.annotate(
            "see here", xy=(3, 0), xytext=(4, 0.5), arrowprops=dict(facecolor="black", shrink=0.05)
        )
        ax.legend()
        fig.tight_layout()

        self.assertConversionRight(fig)

    def test_annotation_arrow(self):
        fig, ax = plt.subplots(1, 1)

        ax.plot(*get_data(), color=COLORS[1], linestyle="none", marker="x", label="data")
        ax.plot(*get_data(), label="fit")

        ax.annotate("", xy=(3, 0), xytext=(4, 0.5), arrowprops=dict(facecolor="black", shrink=0.05))
        ax.legend()
        fig.tight_layout()

        self.assertConversionRight(fig)

    def test_grid_simple(self):
        fig, ax = plt.subplots(1, 1)

        ax.plot(*get_data(), color=COLORS[1], linestyle="none", marker="x", label="data")
        ax.plot(*get_data(), label="fit")

        ax.grid()
        ax.legend()

        fig.tight_layout()

        self.assertConversionRight(fig)
