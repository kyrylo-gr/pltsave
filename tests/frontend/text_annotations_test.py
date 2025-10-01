import matplotlib.pyplot as plt
import numpy as np

from ..test_utils import BaseTest, COLORS, get_data


class TextAnnotationsTest(BaseTest):
    def test_basic_text(self):
        fig, ax = plt.subplots(1, 1)

        x, y = get_data()
        ax.plot(x, y, color=COLORS[0])

        # Basic text placement
        ax.text(1, 0.5, "Simple Text", fontsize=12)
        ax.text(3, -0.3, "Colored Text", fontsize=12, color=COLORS[1])
        ax.text(5, 0.2, "Bold Text", fontsize=12, fontweight="bold")

        ax.set_title("Basic Text")

        self.assertConversionRight(fig)

    def test_text_positioning(self):
        fig, ax = plt.subplots(1, 1)

        x, y = get_data()
        ax.plot(x, y, color=COLORS[0])

        # Different text alignments
        ax.text(
            2,
            0.5,
            "Left Aligned",
            ha="left",
            va="center",
            # bbox=dict(boxstyle="round,pad=0.3", facecolor=COLORS[1], alpha=0.3),
        )
        ax.text(
            4,
            0.5,
            "Center Aligned",
            ha="center",
            va="center",
            # bbox=dict(boxstyle="round,pad=0.3", facecolor=COLORS[2], alpha=0.3),
        )
        ax.text(
            6,
            0.5,
            "Right Aligned",
            ha="right",
            va="center",
            # bbox=dict(boxstyle="round,pad=0.3", facecolor=COLORS[3], alpha=0.3),
        )

        ax.set_title("Text Positioning")

        self.assertConversionRight(fig)

    def test_math_expressions(self):
        fig, ax = plt.subplots(1, 1)

        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(x)
        ax.plot(x, y, color=COLORS[0])

        # Mathematical expressions
        ax.text(1, 0.8, r"$\sin(x)$", fontsize=16)
        ax.text(3, 0.6, r"$\alpha + \beta = \gamma$", fontsize=14)
        ax.text(
            5, 0.4, r"$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$", fontsize=12
        )
        ax.text(1, -0.8, r"$\frac{1}{2\pi} \sum_{n=0}^{\infty} x^n$", fontsize=14)

        ax.set_title("Mathematical Expressions")

        self.assertConversionRight(fig)

    def test_annotations_with_arrows(self):
        fig, ax = plt.subplots(1, 1)

        x, y = get_data()
        ax.plot(x, y, color=COLORS[0])

        # Find peak
        peak_idx = np.argmax(y)
        peak_x, peak_y = x[peak_idx], y[peak_idx]

        # Annotate peak
        ax.annotate(
            "Peak",
            xy=(peak_x, peak_y),
            xytext=(peak_x + 1, peak_y + 0.3),
            arrowprops=dict(arrowstyle="->", color=COLORS[1], lw=2),
            fontsize=12,
            color=COLORS[1],
        )

        # Annotate minimum
        min_idx = np.argmin(y)
        min_x, min_y = x[min_idx], y[min_idx]

        ax.annotate(
            "Minimum",
            xy=(min_x, min_y),
            xytext=(min_x - 1, min_y - 0.3),
            arrowprops=dict(arrowstyle="->", color=COLORS[2], lw=2),
            fontsize=12,
            color=COLORS[2],
        )

        ax.set_title("Annotations with Arrows")

        self.assertConversionRight(fig)

    def test_arrow_styles(self):
        fig, ax = plt.subplots(1, 1)

        x, y = get_data()
        ax.plot(x, y, color=COLORS[0])

        # Different arrow styles
        arrow_styles = ["->", "<->", "<-", "-|>", "<|-"]

        for i, style in enumerate(arrow_styles):
            ax.annotate(
                f"Style: {style}",
                xy=(1 + i, 0.3),
                xytext=(1 + i, 0.6),
                arrowprops=dict(arrowstyle=style, color=COLORS[i % len(COLORS)]),
                ha="center",
            )

        ax.set_title("Arrow Styles")

        self.assertConversionRight(fig)

    # def test_text_boxes(self):
    #     # TODO: add support for bbox
    #     fig, ax = plt.subplots(1, 1)

    #     x, y = get_data()
    #     ax.plot(x, y, color=COLORS[0])

    #     # Different text box styles
    #     ax.text(
    #         1,
    #         0.7,
    #         "Round Box",
    #         bbox=dict(boxstyle="round,pad=0.3", facecolor=COLORS[1], alpha=0.7),
    #     )

    #     ax.text(
    #         3,
    #         0.5,
    #         "Square Box",
    #         bbox=dict(boxstyle="square,pad=0.3", facecolor=COLORS[2], alpha=0.7),
    #     )

    #     ax.text(
    #         5,
    #         0.3,
    #         "Arrow Box",
    #         bbox=dict(boxstyle="rarrow,pad=0.3", facecolor=COLORS[3], alpha=0.7),
    #     )

    #     ax.text(
    #         2,
    #         -0.5,
    #         "Circle Box",
    #         bbox=dict(boxstyle="circle,pad=0.3", facecolor=COLORS[0], alpha=0.7),
    #     )

    #     ax.set_title("Text Boxes")

    #     self.assertConversionRight(fig)

    def test_rotated_text(self):
        fig, ax = plt.subplots(1, 1)

        x, y = get_data()
        ax.plot(x, y, color=COLORS[0])

        # Rotated text at different angles
        angles = [0, 45, 90, 135, 180]

        for i, angle in enumerate(angles):
            ax.text(
                1 + i,
                0.5,
                f"{angle}°",
                rotation=angle,
                ha="center",
                va="center",
                fontsize=12,
                color=COLORS[i % len(COLORS)],
            )

        ax.set_title("Rotated Text")

        self.assertConversionRight(fig)

    def test_multi_line_text(self):
        fig, ax = plt.subplots(1, 1)

        x, y = get_data()
        ax.plot(x, y, color=COLORS[0])

        # Multi-line text
        multiline_text = """This is line 1
This is line 2
This is line 3"""

        ax.text(
            0.05,
            0.95,
            multiline_text,
            transform=ax.transAxes,
            verticalalignment="top",
            fontsize=10,
            # bbox=dict(boxstyle="round,pad=0.5", facecolor=COLORS[1], alpha=0.7),
        )

        ax.set_title("Multi-line Text")

        self.assertConversionRight(fig)

    def test_coordinate_systems(self):
        fig, ax = plt.subplots(1, 1)

        x, y = get_data()
        ax.plot(x, y, color=COLORS[0])

        # Text in different coordinate systems
        ax.text(
            0.1,
            0.9,
            "Axes coordinates (0.1, 0.9)",
            transform=ax.transAxes,
            fontsize=10,
            color=COLORS[1],
        )

        ax.text(
            0.5,
            0.8,
            "Figure coordinates (0.5, 0.8)",
            transform=fig.transFigure,
            fontsize=10,
            color=COLORS[2],
        )

        ax.text(3, 0.5, "Data coordinates (3, 0.5)", fontsize=10, color=COLORS[3])

        ax.set_title("Coordinate Systems")

        self.assertConversionRight(fig)

    def test_complex_annotations(self):
        fig, ax = plt.subplots(1, 1)

        # Create a more complex plot
        x = np.linspace(0, 2 * np.pi, 100)
        y1 = np.sin(x)
        y2 = np.cos(x)

        ax.plot(x, y1, color=COLORS[0], label="sin(x)")
        ax.plot(x, y2, color=COLORS[1], label="cos(x)")

        # Find intersection points
        intersection_idx = np.argwhere(np.diff(np.sign(y1 - y2))).flatten()

        # Annotate intersections
        for i, idx in enumerate(intersection_idx[:2]):  # Only first 2 intersections
            ax.annotate(
                f"Intersection {i + 1}",
                xy=(x[idx], y1[idx]),
                xytext=(x[idx] + 0.5, y1[idx] + 0.3),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.2"),
                # bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
            )

        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_title("Complex Annotations")

        self.assertConversionRight(fig)
