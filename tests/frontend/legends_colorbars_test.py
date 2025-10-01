import matplotlib.pyplot as plt
import numpy as np

from ..test_utils import BaseTest, COLORS, get_data


class LegendsColorbarsTest(BaseTest):
    def test_basic_legend(self):
        fig, ax = plt.subplots(1, 1)

        x = np.linspace(0, 2 * np.pi, 100)
        ax.plot(x, np.sin(x), color=COLORS[0], label="sin(x)")
        ax.plot(x, np.cos(x), color=COLORS[1], label="cos(x)")
        ax.plot(x, np.tan(x / 2), color=COLORS[2], label="tan(x/2)")

        ax.legend()
        ax.set_title("Basic Legend")
        ax.set_ylim(-2, 2)

        self.assertConversionRight(fig)

    def test_legend_positioning(self):
        fig, axes = plt.subplots(2, 2, figsize=(10, 8))

        x = np.linspace(0, 2 * np.pi, 100)

        # Different legend positions
        positions = ["upper right", "upper left", "lower left", "lower right"]

        for ax, pos in zip(axes.flat, positions):
            ax.plot(x, np.sin(x), color=COLORS[0], label="sin(x)")
            ax.plot(x, np.cos(x), color=COLORS[1], label="cos(x)")
            ax.legend(loc=pos)
            ax.set_title(f"Legend: {pos}")

        fig.tight_layout()
        self.assertConversionRight(fig)

    def test_legend_customization(self):
        fig, ax = plt.subplots(1, 1)

        x = np.linspace(0, 2 * np.pi, 100)
        ax.plot(x, np.sin(x), color=COLORS[0], linewidth=3, label="sin(x)")
        ax.plot(x, np.cos(x), color=COLORS[1], linewidth=3, label="cos(x)")

        # Customized legend
        legend = ax.legend(
            loc="upper right",
            frameon=True,
            fancybox=True,
            shadow=True,
            ncol=2,
            fontsize=12,
            title="Functions",
            title_fontsize=14,
        )
        legend.get_frame().set_facecolor(COLORS[2])
        legend.get_frame().set_alpha(0.8)

        ax.set_title("Customized Legend")

        self.assertConversionRight(fig)

    def test_legend_outside_plot(self):
        fig, ax = plt.subplots(1, 1)

        x = np.linspace(0, 2 * np.pi, 100)
        ax.plot(x, np.sin(x), color=COLORS[0], label="sin(x)")
        ax.plot(x, np.cos(x), color=COLORS[1], label="cos(x)")
        ax.plot(x, np.sin(2 * x), color=COLORS[2], label="sin(2x)")
        ax.plot(x, np.cos(2 * x), color=COLORS[3], label="cos(2x)")

        # Legend outside plot area
        ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
        ax.set_title("Legend Outside Plot")

        fig.tight_layout()
        self.assertConversionRight(fig)

    def test_multiple_legends(self):
        fig, ax = plt.subplots(1, 1)

        x = np.linspace(0, 2 * np.pi, 100)

        # First set of plots
        line1 = ax.plot(x, np.sin(x), color=COLORS[0], label="sin(x)")
        line2 = ax.plot(x, np.cos(x), color=COLORS[1], label="cos(x)")

        # Create first legend
        legend1 = ax.legend(handles=[line1[0], line2[0]], loc="upper right")

        # Second set of plots
        line3 = ax.plot(
            x, np.sin(2 * x), color=COLORS[2], linestyle="--", label="sin(2x)"
        )
        line4 = ax.plot(
            x, np.cos(2 * x), color=COLORS[3], linestyle="--", label="cos(2x)"
        )

        # Create second legend and add first legend back
        legend2 = ax.legend(handles=[line3[0], line4[0]], loc="lower right")
        ax.add_artist(legend1)

        ax.set_title("Multiple Legends")

        self.assertConversionRight(fig)

    def test_colorbar_basic(self):
        fig, ax = plt.subplots(1, 1)

        # Create 2D data
        x = np.linspace(0, 5, 50)
        y = np.linspace(0, 5, 50)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(X) * np.cos(Y)

        # Plot with colorbar
        im = ax.imshow(Z, extent=[0, 5, 0, 5], cmap="viridis", origin="lower")
        cbar = fig.colorbar(im, ax=ax)
        cbar.set_label("Intensity", rotation=270, labelpad=15)

        ax.set_title("Basic Colorbar")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

        self.assertConversionRight(fig)

    def test_colorbar_customization(self):
        fig, ax = plt.subplots(1, 1)

        # Create scatter plot with color mapping
        x, y = get_data(100)
        colors = np.sqrt(x**2 + y**2)

        scatter = ax.scatter(x, y, c=colors, cmap="plasma", s=50, alpha=0.7)

        # Customized colorbar
        cbar = fig.colorbar(scatter, ax=ax, shrink=0.8, pad=0.1)
        cbar.set_label("Distance from Origin", fontsize=12)
        cbar.ax.tick_params(labelsize=10)

        # Custom colorbar ticks
        cbar.set_ticks([colors.min(), colors.mean(), colors.max()])
        cbar.set_ticklabels(["Min", "Mean", "Max"])

        ax.set_title("Customized Colorbar")

        self.assertConversionRight(fig)

    def test_colorbar_positioning(self):
        fig, axes = plt.subplots(2, 2, figsize=(10, 8))

        # Create test data
        x = np.linspace(0, 1, 20)
        y = np.linspace(0, 1, 20)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(2 * np.pi * X) * np.cos(2 * np.pi * Y)

        # Different colorbar orientations and positions
        im1 = axes[0, 0].imshow(Z, cmap="coolwarm")
        cbar1 = fig.colorbar(im1, ax=axes[0, 0], orientation="vertical", shrink=0.8)
        axes[0, 0].set_title("Vertical Colorbar")

        im2 = axes[0, 1].imshow(Z, cmap="hot")
        cbar2 = fig.colorbar(im2, ax=axes[0, 1], orientation="horizontal", shrink=0.8)
        axes[0, 1].set_title("Horizontal Colorbar")

        im3 = axes[1, 0].imshow(Z, cmap="viridis")
        cbar3 = fig.colorbar(im3, ax=axes[1, 0], shrink=0.6, pad=0.2)
        axes[1, 0].set_title("Colorbar with Padding")

        im4 = axes[1, 1].imshow(Z, cmap="magma")
        cbar4 = fig.colorbar(im4, ax=axes[1, 1], shrink=0.4, aspect=10)
        axes[1, 1].set_title("Colorbar Custom Aspect")

        fig.tight_layout()
        self.assertConversionRight(fig)

    def test_shared_colorbar(self):
        fig, axes = plt.subplots(1, 3, figsize=(12, 4))

        # Create different datasets with same scale
        x = np.linspace(-2, 2, 20)
        y = np.linspace(-2, 2, 20)
        X, Y = np.meshgrid(x, y)

        Z1 = np.sin(X) * np.cos(Y)
        Z2 = np.cos(X) * np.sin(Y)
        Z3 = np.sin(X * Y)

        # Plot all with same colormap and scale
        vmin, vmax = -1, 1
        im1 = axes[0].imshow(Z1, vmin=vmin, vmax=vmax, cmap="RdBu")
        axes[0].set_title("sin(X)cos(Y)")

        im2 = axes[1].imshow(Z2, vmin=vmin, vmax=vmax, cmap="RdBu")
        axes[1].set_title("cos(X)sin(Y)")

        im3 = axes[2].imshow(Z3, vmin=vmin, vmax=vmax, cmap="RdBu")
        axes[2].set_title("sin(XY)")

        # Shared colorbar
        fig.colorbar(im1, ax=axes, orientation="horizontal", fraction=0.05, pad=0.1)

        fig.suptitle("Shared Colorbar")
        fig.tight_layout()

        self.assertConversionRight(fig)

    def test_discrete_colorbar(self):
        fig, ax = plt.subplots(1, 1)

        # Create categorical data
        x = np.random.rand(100)
        y = np.random.rand(100)
        categories = np.random.randint(0, 5, 100)

        scatter = ax.scatter(x, y, c=categories, cmap="Set1", s=50)

        # Discrete colorbar
        cbar = fig.colorbar(scatter, ax=ax, ticks=range(5))
        cbar.set_label("Category")
        cbar.set_ticklabels(["Cat A", "Cat B", "Cat C", "Cat D", "Cat E"])

        ax.set_title("Discrete Colorbar")

        self.assertConversionRight(fig)
