import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator, FuncFormatter

from ..test_utils import BaseTest, COLORS, get_data


class AxesFormattingTest(BaseTest):
    def test_custom_ticks(self):
        fig, ax = plt.subplots(1, 1)

        x, y = get_data()
        ax.plot(x, y, color=COLORS[0])

        # Custom tick positions and labels
        ax.set_xticks([0, 1, 2, 3, 4, 5, 6])
        ax.set_xticklabels(["A", "B", "C", "D", "E", "F", "G"])
        ax.set_yticks([-1, -0.5, 0, 0.5, 1])

        ax.set_title("Custom Ticks")

        self.assertConversionRight(fig)

    def test_tick_formatting(self):
        fig, ax = plt.subplots(1, 1)

        x = np.linspace(0, 1000, 100)
        y = x**2
        ax.plot(x, y, color=COLORS[0])

        # Format ticks
        ax.ticklabel_format(style="scientific", axis="y", scilimits=(0, 0))
        ax.tick_params(axis="x", rotation=45)
        ax.tick_params(axis="both", which="major", labelsize=12)

        ax.set_title("Tick Formatting")

        self.assertConversionRight(fig)

    def test_log_scale(self):
        fig, ax = plt.subplots(1, 1)

        x = np.logspace(0, 3, 100)
        y = x**2

        ax.loglog(x, y, color=COLORS[0], linewidth=2)
        ax.set_title("Log-Log Scale")
        ax.set_xlabel("X (log scale)")
        ax.set_ylabel("Y (log scale)")
        ax.grid(True, alpha=0.3)

        self.assertConversionRight(fig)

    def test_semilog_scales(self):
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))

        x = np.linspace(1, 100, 100)
        y = np.exp(x / 20)

        # Semi-log x
        axes[0].semilogx(x, y, color=COLORS[0])
        axes[0].set_title("Semi-log X")
        axes[0].grid(True, alpha=0.3)

        # Semi-log y
        axes[1].semilogy(x, y, color=COLORS[1])
        axes[1].set_title("Semi-log Y")
        axes[1].grid(True, alpha=0.3)

        fig.tight_layout()
        self.assertConversionRight(fig)

    def test_spine_customization(self):
        fig, ax = plt.subplots(1, 1)

        x, y = get_data()
        ax.plot(x, y, color=COLORS[0])

        # Customize spines
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(COLORS[1])
        ax.spines["bottom"].set_color(COLORS[1])
        ax.spines["left"].set_linewidth(2)
        ax.spines["bottom"].set_linewidth(2)

        ax.set_title("Custom Spines")

        self.assertConversionRight(fig)

    def test_axis_limits(self):
        fig, ax = plt.subplots(1, 1)

        x, y = get_data()
        ax.plot(x, y, color=COLORS[0])

        # Set custom limits
        ax.set_xlim(1, 5)
        ax.set_ylim(-0.5, 0.8)

        ax.set_title("Custom Axis Limits")

        self.assertConversionRight(fig)

    def test_inverted_axes(self):
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))

        x, y = get_data()

        # Normal plot
        axes[0].plot(x, y, color=COLORS[0])
        axes[0].set_title("Normal Axes")

        # Inverted axes
        axes[1].plot(x, y, color=COLORS[1])
        axes[1].invert_xaxis()
        axes[1].invert_yaxis()
        axes[1].set_title("Inverted Axes")

        fig.tight_layout()
        self.assertConversionRight(fig)

    def test_shared_axes(self):
        fig, axes = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(8, 8))

        # Generate different data for each subplot
        for i, ax in enumerate(axes.flat):
            x = np.linspace(0, 2 * np.pi, 100)
            y = np.sin(x + i * np.pi / 4)
            ax.plot(x, y, color=COLORS[i % len(COLORS)])
            ax.set_title(f"Subplot {i + 1}")

        # Only the bottom subplots will have x labels
        # Only the left subplots will have y labels
        axes[1, 0].set_xlabel("X axis")
        axes[1, 1].set_xlabel("X axis")
        axes[0, 0].set_ylabel("Y axis")
        axes[1, 0].set_ylabel("Y axis")

        fig.suptitle("Shared Axes")
        fig.tight_layout()

        self.assertConversionRight(fig)

    def test_secondary_axes(self):
        fig, ax1 = plt.subplots(1, 1)

        x = np.linspace(0, 2 * np.pi, 100)
        y1 = np.sin(x)

        # Primary axis
        ax1.plot(x, y1, color=COLORS[0], label="sin(x)")
        ax1.set_xlabel("X")
        ax1.set_ylabel("sin(x)", color=COLORS[0])
        ax1.tick_params(axis="y", labelcolor=COLORS[0])

        # Secondary axis
        ax2 = ax1.twinx()
        y2 = np.cos(x) * 100
        ax2.plot(x, y2, color=COLORS[1], label="100*cos(x)")
        ax2.set_ylabel("100*cos(x)", color=COLORS[1])
        ax2.tick_params(axis="y", labelcolor=COLORS[1])

        ax1.set_title("Secondary Y-Axis")

        # Combine legends
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

        self.assertConversionRight(fig)

    def test_aspect_ratio(self):
        fig, axes = plt.subplots(1, 3, figsize=(12, 4))

        # Circle data
        theta = np.linspace(0, 2 * np.pi, 100)
        x = np.cos(theta)
        y = np.sin(theta)

        # Auto aspect
        axes[0].plot(x, y, color=COLORS[0])
        axes[0].set_title("Auto Aspect")

        # Equal aspect
        axes[1].plot(x, y, color=COLORS[1])
        axes[1].set_aspect("equal")
        axes[1].set_title("Equal Aspect")

        # Custom aspect
        axes[2].plot(x, y, color=COLORS[2])
        axes[2].set_aspect(0.5)
        axes[2].set_title("Custom Aspect (0.5)")

        fig.tight_layout()
        self.assertConversionRight(fig)
