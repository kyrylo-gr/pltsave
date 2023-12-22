import matplotlib.pyplot as plt

import pltsave
from ..test_utils import BaseTest, create_simple_plot, plot_on_axis


class CompareFunctionTest(BaseTest):
    def test_simple_figure(self):
        fig, _ = create_simple_plot()

        self.assertConversionRight(fig)

    def test_wrong_title(self):
        fig, ax = create_simple_plot()

        fig2 = pltsave.loads(pltsave.dumps(fig))

        ax.set(title="Some title")

        self.assertFigNotEqual(fig, fig2)

    def test_wrong_xlabel(self):
        fig, ax = create_simple_plot()

        fig2 = pltsave.loads(pltsave.dumps(fig))

        ax.set(xlabel="Some title")

        self.assertFigNotEqual(fig, fig2)

    def test_wrong_ylabel(self):
        fig, ax = create_simple_plot()

        fig2 = pltsave.loads(pltsave.dumps(fig))

        ax.set(ylabel="Some title")

        self.assertFigNotEqual(fig, fig2)


class SimplePlotTest(BaseTest):
    def test_simple_figure_with_labels(self):
        fig, _ = create_simple_plot(
            title="Some title", xlabel="x", ylabel="y")

        self.assertConversionRight(fig)


class SubplotsTest(BaseTest):
    def test_2_rows_subplots(self):
        fig, axes = plt.subplots(2, 1)

        for i, ax in enumerate(axes):
            plot_on_axis(ax, title=f"Plot {i}",
                         xlabel=f"x_{i}", ylabel=f"y_{i}")
        fig.tight_layout()
        self.assertConversionRight(fig)

    def test_2_cols_subplots(self):
        fig, axes = plt.subplots(1, 2)

        for i, ax in enumerate(axes):
            plot_on_axis(ax, title=f"Plot {i}",
                         xlabel=f"x_{i}", ylabel=f"y_{i}")
        fig.tight_layout()
        self.assertConversionRight(fig)

    def test_2x2_grid_subplots(self):
        fig, axes = plt.subplots(2, 2)
        axes = axes.flatten()

        for i, ax in enumerate(axes):
            plot_on_axis(ax, title=f"Plot {i}",
                         xlabel=f"x_{i}", ylabel=f"y_{i}")
        fig.tight_layout()
        self.assertConversionRight(fig)


class SetLimitsTest(BaseTest):
    def test_set_xlim(self):
        fig, ax = create_simple_plot()
        ax.set_xlim(0, ax.get_xlim()[1]/2)

        self.assertConversionRight(fig)

    def test_set_ylim(self):
        fig, ax = create_simple_plot()
        ax.set_ylim(0, ax.get_ylim()[1]/2)

        self.assertConversionRight(fig)
