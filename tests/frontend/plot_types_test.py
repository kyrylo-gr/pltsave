import matplotlib.pyplot as plt
import numpy as np

from ..test_utils import BaseTest, COLORS, get_data


class PlotTypesTest(BaseTest):
    def test_scatter_plot(self):
        fig, ax = plt.subplots(1, 1)

        x, y = get_data(50)
        ax.scatter(x, y, c=COLORS[1], alpha=0.6, s=50, ec=COLORS[0])
        ax.set_title("Scatter Plot")
        ax.set_xlabel("X values")
        ax.set_ylabel("Y values")

        self.assertConversionRight(fig)

    def test_bar_plot(self):
        fig, ax = plt.subplots(1, 1)

        categories = ["A", "B", "C", "D", "E"]
        values = [23, 45, 56, 78, 32]

        ax.bar(categories, values, color=COLORS[: len(categories)])
        ax.set_title("Bar Plot")
        ax.set_xlabel("Categories")
        ax.set_ylabel("Values")

        self.assertConversionRight(fig)

    def test_horizontal_bar_plot(self):
        fig, ax = plt.subplots(1, 1)

        categories = ["A", "B", "C", "D", "E"]
        values = [23, 45, 56, 78, 32]

        ax.barh(categories, values, color=COLORS[: len(categories)])
        ax.set_title("Horizontal Bar Plot")
        ax.set_xlabel("Values")
        ax.set_ylabel("Categories")

        self.assertConversionRight(fig)

    def test_histogram(self):
        fig, ax = plt.subplots(1, 1)

        data = np.random.normal(0, 1, 1000)
        ax.hist(data, bins=30, alpha=0.7, color=COLORS[0], edgecolor="black")
        ax.set_title("Histogram")
        ax.set_xlabel("Value")
        ax.set_ylabel("Frequency")

        self.assertConversionRight(fig)

    def test_pie_chart(self):
        fig, ax = plt.subplots(1, 1)

        sizes = [15, 30, 45, 10]
        labels = ["Frogs", "Hogs", "Dogs", "Logs"]
        explode = (0, 0.1, 0, 0)  # explode 2nd slice

        ax.pie(
            sizes,
            explode=explode,
            labels=labels,
            colors=COLORS[: len(sizes)],
            autopct="%1.1f%%",
            shadow=True,
            startangle=90,
        )
        ax.set_title("Pie Chart")

        self.assertConversionRight(fig)

    def test_stem_plot(self):
        fig, ax = plt.subplots(1, 1)

        x = np.linspace(0.1, 2 * np.pi, 10)
        y = np.cos(x)

        ax.stem(x, y, linefmt=COLORS[0], markerfmt="o", basefmt=" ")
        ax.set_title("Stem Plot")
        ax.set_xlabel("X values")
        ax.set_ylabel("Y values")

        self.assertConversionRight(fig)

    def test_step_plot(self):
        fig, ax = plt.subplots(1, 1)

        x = np.arange(1, 7, 0.4)
        y = np.sin(x)

        ax.step(x, y, color=COLORS[0], linewidth=2, where="mid")
        ax.set_title("Step Plot")
        ax.set_xlabel("X values")
        ax.set_ylabel("Y values")

        self.assertConversionRight(fig)

    def test_fill_between(self):
        fig, ax = plt.subplots(1, 1)

        x = np.linspace(0, 2 * np.pi, 100)
        y1 = np.sin(x)
        y2 = np.cos(x)

        ax.plot(x, y1, color=COLORS[0], label="sin(x)")
        ax.plot(x, y2, color=COLORS[1], label="cos(x)")
        ax.fill_between(x, y1, y2, alpha=0.3, color=COLORS[2])
        ax.set_title("Fill Between")
        ax.legend()

        self.assertConversionRight(fig)

    def test_multiple_plot_types(self):
        fig, axes = plt.subplots(2, 2, figsize=(10, 8))

        # Line plot
        x, y = get_data()
        axes[0, 0].plot(x, y, color=COLORS[0])
        axes[0, 0].set_title("Line Plot")

        # Scatter plot
        x_scatter, y_scatter = get_data(50)
        axes[0, 1].scatter(x_scatter, y_scatter, c=COLORS[1], alpha=0.6)
        axes[0, 1].set_title("Scatter Plot")

        # Bar plot
        categories = ["A", "B", "C", "D"]
        values = [23, 45, 56, 78]
        axes[1, 0].bar(categories, values, color=COLORS[2])
        axes[1, 0].set_title("Bar Plot")

        # Histogram
        data = np.random.normal(0, 1, 500)
        axes[1, 1].hist(data, bins=20, alpha=0.7, color=COLORS[3])
        axes[1, 1].set_title("Histogram")

        fig.tight_layout()
        self.assertConversionRight(fig)
