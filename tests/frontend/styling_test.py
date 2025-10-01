import matplotlib.pyplot as plt
import numpy as np

from ..test_utils import BaseTest, COLORS, get_data


class StylingTest(BaseTest):
    def test_line_styles(self):
        fig, ax = plt.subplots(1, 1)

        x = np.linspace(0, 2 * np.pi, 100)

        # Different line styles
        ax.plot(x, np.sin(x), linestyle="-", color=COLORS[0], label="solid")
        ax.plot(x, np.sin(x) + 0.5, linestyle="--", color=COLORS[1], label="dashed")
        ax.plot(x, np.sin(x) + 1.0, linestyle="-.", color=COLORS[2], label="dashdot")
        ax.plot(x, np.sin(x) + 1.5, linestyle=":", color=COLORS[3], label="dotted")

        ax.set_title("Line Styles")
        ax.legend()

        self.assertConversionRight(fig)

    def test_line_widths(self):
        fig, ax = plt.subplots(1, 1)

        x = np.linspace(0, 2 * np.pi, 100)

        # Different line widths
        ax.plot(x, np.sin(x), linewidth=1, color=COLORS[0], label="width=1")
        ax.plot(x, np.sin(x) + 0.5, linewidth=2, color=COLORS[1], label="width=2")
        ax.plot(x, np.sin(x) + 1.0, linewidth=3, color=COLORS[2], label="width=3")
        ax.plot(x, np.sin(x) + 1.5, linewidth=5, color=COLORS[3], label="width=5")

        ax.set_title("Line Widths")
        ax.legend()

        self.assertConversionRight(fig)

    def test_markers(self):
        fig, ax = plt.subplots(1, 1)

        x = np.linspace(0, 2 * np.pi, 20)

        # Different markers
        ax.plot(
            x, np.sin(x), marker="o", linestyle="none", color=COLORS[0], label="circle"
        )
        ax.plot(
            x,
            np.sin(x) + 0.5,
            marker="s",
            linestyle="none",
            color=COLORS[1],
            label="square",
        )
        ax.plot(
            x,
            np.sin(x) + 1.0,
            marker="^",
            linestyle="none",
            color=COLORS[2],
            label="triangle",
        )
        ax.plot(
            x,
            np.sin(x) + 1.5,
            marker="*",
            linestyle="none",
            color=COLORS[3],
            label="star",
        )

        ax.set_title("Markers")
        ax.legend()

        self.assertConversionRight(fig)

    def test_marker_properties(self):
        fig, ax = plt.subplots(1, 1)

        x = np.linspace(0, 2 * np.pi, 20)
        y = np.sin(x)

        ax.plot(
            x,
            y,
            marker="o",
            markersize=8,
            markerfacecolor=COLORS[0],
            markeredgecolor=COLORS[1],
            markeredgewidth=2,
            linestyle="none",
        )

        ax.set_title("Marker Properties")

        self.assertConversionRight(fig)

    def test_alpha_transparency(self):
        fig, ax = plt.subplots(1, 1)

        x = np.linspace(0, 2 * np.pi, 100)

        # Different alpha values
        ax.plot(
            x, np.sin(x), color=COLORS[0], alpha=1.0, linewidth=5, label="alpha=1.0"
        )
        ax.plot(
            x,
            np.sin(x) + 0.5,
            color=COLORS[1],
            alpha=0.7,
            linewidth=5,
            label="alpha=0.7",
        )
        ax.plot(
            x,
            np.sin(x) + 1.0,
            color=COLORS[2],
            alpha=0.4,
            linewidth=5,
            label="alpha=0.4",
        )
        ax.plot(
            x,
            np.sin(x) + 1.5,
            color=COLORS[3],
            alpha=0.1,
            linewidth=5,
            label="alpha=0.1",
        )

        ax.set_title("Alpha Transparency")
        ax.legend()

        self.assertConversionRight(fig)

    def test_color_formats(self):
        fig, ax = plt.subplots(1, 1)

        x = np.linspace(0, 2 * np.pi, 100)

        # Different color formats
        ax.plot(x, np.sin(x), color="red", label="named color")
        ax.plot(x, np.sin(x) + 0.5, color="#00ff00", label="hex color")
        ax.plot(x, np.sin(x) + 1.0, color=(0, 0, 1), label="RGB tuple")
        ax.plot(x, np.sin(x) + 1.5, color=(1, 0, 1, 0.5), label="RGBA tuple")

        ax.set_title("Color Formats")
        ax.legend()

        self.assertConversionRight(fig)

    def test_font_properties(self):
        fig, ax = plt.subplots(1, 1)

        x, y = get_data()
        ax.plot(x, y, color=COLORS[0])

        # Different font properties
        ax.set_title("Font Properties Test", fontsize=16, fontweight="bold")
        ax.set_xlabel("X Label", fontsize=12, fontstyle="italic")
        ax.set_ylabel("Y Label", fontsize=14, fontfamily="serif")

        # Add text with different fonts
        ax.text(0.5, 0.5, "Default font", transform=ax.transAxes)
        ax.text(0.5, 0.4, "Bold text", transform=ax.transAxes, fontweight="bold")
        ax.text(0.5, 0.3, "Italic text", transform=ax.transAxes, fontstyle="italic")

        self.assertConversionRight(fig)

    def test_grid_styles(self):
        fig, ax = plt.subplots(1, 1)

        x, y = get_data()
        ax.plot(x, y, color=COLORS[0])

        # Grid with custom styling
        ax.grid(True, linestyle="--", alpha=0.7, color="gray", linewidth=0.5)
        ax.set_title("Custom Grid Styling")

        self.assertConversionRight(fig)

    def test_fill_styles(self):
        fig, ax = plt.subplots(1, 1)

        x = np.linspace(0, 2 * np.pi, 100)
        y1 = np.sin(x)
        y2 = np.cos(x)

        # Fill between with different styles
        ax.fill_between(x, y1, alpha=0.3, color=COLORS[0], label="fill area")
        ax.fill_between(
            x, 0, y2, alpha=0.5, color=COLORS[1], hatch="///", label="hatched fill"
        )

        ax.plot(x, y1, color=COLORS[0], linewidth=2)
        ax.plot(x, y2, color=COLORS[1], linewidth=2)

        ax.set_title("Fill Styles")
        ax.legend()

        self.assertConversionRight(fig)

    def test_scatter_styling(self):
        fig, ax = plt.subplots(1, 1)

        x, y = get_data(50)

        # Scatter plot with varied sizes and colors
        sizes = np.random.randint(20, 200, len(x))
        colors = np.random.rand(len(x))

        scatter = ax.scatter(
            x, y, s=sizes, c=colors, alpha=0.6, cmap="viridis", edgecolors="black"
        )
        ax.set_title("Styled Scatter Plot")
        fig.colorbar(scatter, ax=ax, label="Color value")

        self.assertConversionRight(fig)
