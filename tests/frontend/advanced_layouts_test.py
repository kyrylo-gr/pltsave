import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

from ..test_utils import BaseTest, COLORS, get_data


class AdvancedLayoutsTest(BaseTest):
    def test_gridspec_basic(self):
        fig = plt.figure(figsize=(10, 8))
        gs = gridspec.GridSpec(3, 3, figure=fig)

        # Different sized subplots
        ax1 = fig.add_subplot(gs[0, :])  # Top row, all columns
        ax2 = fig.add_subplot(gs[1, :-1])  # Middle row, first two columns
        ax3 = fig.add_subplot(gs[1:, -1])  # Last column, bottom two rows
        ax4 = fig.add_subplot(gs[-1, 0])  # Bottom left
        ax5 = fig.add_subplot(gs[-1, 1])  # Bottom middle

        # Plot data in each subplot
        x, y = get_data()

        ax1.plot(x, y, color=COLORS[0])
        ax1.set_title("Spanning Top Row")

        ax2.scatter(x[::5], y[::5], color=COLORS[1])
        ax2.set_title("Middle Left")

        ax3.bar(range(5), [1, 3, 2, 4, 2], color=COLORS[2])
        ax3.set_title("Right Column")

        ax4.hist(np.random.normal(0, 1, 100), bins=20, alpha=0.7, color=COLORS[3])
        ax4.set_title("Bottom Left")

        ax5.pie([1, 2, 3, 4], labels=["A", "B", "C", "D"], colors=COLORS)
        ax5.set_title("Bottom Middle")

        fig.suptitle("GridSpec Layout")
        fig.tight_layout()

        self.assertConversionRight(fig)

    def test_gridspec_spacing(self):
        fig = plt.figure(figsize=(10, 8))
        gs = gridspec.GridSpec(
            2,
            2,
            figure=fig,
            width_ratios=[1, 2],
            height_ratios=[2, 1],
            wspace=0.3,
            hspace=0.4,
        )

        axes = [fig.add_subplot(gs[i, j]) for i in range(2) for j in range(2)]

        # Plot different data in each subplot
        for i, ax in enumerate(axes):
            x = np.linspace(0, 2 * np.pi, 100)
            y = np.sin(x + i * np.pi / 4)
            ax.plot(x, y, color=COLORS[i])
            ax.set_title(f"Subplot {i + 1}")
            ax.grid(True, alpha=0.3)

        fig.suptitle("GridSpec with Custom Spacing")

        self.assertConversionRight(fig)

    def test_nested_gridspec(self):
        fig = plt.figure(figsize=(12, 8))

        # Outer grid
        outer_gs = gridspec.GridSpec(2, 2, figure=fig, wspace=0.2, hspace=0.3)

        # Top left: single plot
        ax1 = fig.add_subplot(outer_gs[0, 0])
        x, y = get_data()
        ax1.plot(x, y, color=COLORS[0])
        ax1.set_title("Single Plot")

        # Top right: nested grid
        inner_gs1 = gridspec.GridSpecFromSubplotSpec(
            2, 2, outer_gs[0, 1], wspace=0.1, hspace=0.1
        )

        for i in range(4):
            ax = fig.add_subplot(inner_gs1[i // 2, i % 2])
            data = np.random.random(20)
            ax.plot(data, color=COLORS[i % len(COLORS)])
            ax.set_title(f"Nested {i + 1}")

        # Bottom: spanning both columns
        ax2 = fig.add_subplot(outer_gs[1, :])
        x = np.linspace(0, 2 * np.pi, 100)
        for i in range(3):
            y = np.sin(x + i * np.pi / 3)
            ax2.plot(x, y, color=COLORS[i], label=f"sin(x + {i}π/3)")
        ax2.legend()
        ax2.set_title("Spanning Bottom")

        fig.suptitle("Nested GridSpec")

        self.assertConversionRight(fig)

    def test_subplot_mosaic(self):
        # Create a complex layout using subplot_mosaic
        mosaic = """
        AAB
        CCB
        CDD
        """

        fig, axes = plt.subplot_mosaic(mosaic, figsize=(10, 8))

        # Plot A: Line plot
        x, y = get_data()
        axes["A"].plot(x, y, color=COLORS[0])
        axes["A"].set_title("Area A - Line Plot")

        # Plot B: Vertical bar plot
        categories = ["X", "Y", "Z", "W"]
        values = [15, 25, 20, 30]
        axes["B"].barh(categories, values, color=COLORS[1])
        axes["B"].set_title("Area B - Horizontal Bars")

        # Plot C: Scatter plot
        x_scatter = np.random.rand(50)
        y_scatter = np.random.rand(50)
        axes["C"].scatter(x_scatter, y_scatter, color=COLORS[2], alpha=0.6)
        axes["C"].set_title("Area C - Scatter Plot")

        # Plot D: Pie chart
        sizes = [30, 25, 25, 20]
        axes["D"].pie(
            sizes, labels=["A", "B", "C", "D"], colors=COLORS, autopct="%1.1f%%"
        )
        axes["D"].set_title("Area D - Pie Chart")

        fig.suptitle("Subplot Mosaic Layout")
        fig.tight_layout()

        self.assertConversionRight(fig)

    def test_figure_subplots_with_ratios(self):
        fig, axes = plt.subplots(
            2,
            3,
            figsize=(12, 8),
            gridspec_kw={"width_ratios": [1, 2, 1], "height_ratios": [2, 1]},
        )

        # Fill each subplot with different plot types
        plot_types = ["line", "scatter", "bar", "hist", "pie", "step"]

        for i, (ax, plot_type) in enumerate(zip(axes.flat, plot_types)):
            if plot_type == "line":
                x, y = get_data()
                ax.plot(x, y, color=COLORS[i % len(COLORS)])
            elif plot_type == "scatter":
                x = np.random.rand(30)
                y = np.random.rand(30)
                ax.scatter(x, y, color=COLORS[i % len(COLORS)])
            elif plot_type == "bar":
                x = range(5)
                y = np.random.randint(1, 10, 5)
                ax.bar(x, y, color=COLORS[i % len(COLORS)])
            elif plot_type == "hist":
                data = np.random.normal(0, 1, 100)
                ax.hist(data, bins=15, alpha=0.7, color=COLORS[i % len(COLORS)])
            elif plot_type == "pie":
                sizes = [25, 25, 25, 25]
                ax.pie(sizes, colors=COLORS)
            elif plot_type == "step":
                x = np.linspace(0, 10, 20)
                y = np.sin(x)
                ax.step(x, y, color=COLORS[i % len(COLORS)])

            ax.set_title(f"{plot_type.title()} Plot")

        fig.suptitle("Subplots with Custom Ratios")
        fig.tight_layout()

        self.assertConversionRight(fig)

    def test_inset_plots(self):
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))

        # Main plot
        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(x) + 0.1 * np.random.random(100)
        ax.plot(x, y, color=COLORS[0], alpha=0.7)
        ax.set_title("Main Plot with Inset")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

        # Create inset
        from mpl_toolkits.axes_grid1.inset_locator import inset_axes

        axins = inset_axes(ax, width="40%", height="40%", loc="upper right")

        # Zoom in on a specific region
        x_zoom = x[(x >= 1) & (x <= 2)]
        y_zoom = y[(x >= 1) & (x <= 2)]
        axins.plot(x_zoom, y_zoom, color=COLORS[1])
        axins.set_xlim(1, 2)
        axins.set_ylim(y_zoom.min() - 0.1, y_zoom.max() + 0.1)
        axins.set_title("Zoomed View", fontsize=10)

        # Mark the region being zoomed
        ax.indicate_inset_zoom(axins, edgecolor="black", alpha=0.7)

        self.assertConversionRight(fig)

    def test_constrained_layout(self):
        fig = plt.figure(figsize=(10, 8), constrained_layout=True)
        gs = fig.add_gridspec(3, 3)

        # Create subplots with different sizes
        ax1 = fig.add_subplot(gs[0, :2])
        ax2 = fig.add_subplot(gs[0, 2])
        ax3 = fig.add_subplot(gs[1, :])
        ax4 = fig.add_subplot(gs[2, 0])
        ax5 = fig.add_subplot(gs[2, 1:])

        # Add plots with long labels to test layout
        x, y = get_data()

        ax1.plot(x, y, color=COLORS[0])
        ax1.set_title("Very Long Title That Might Overlap Without Proper Layout")
        ax1.set_ylabel("Very Long Y Label That Takes Space")

        ax2.scatter(x[::10], y[::10], color=COLORS[1])
        ax2.set_title("Scatter")

        ax3.bar(range(10), np.random.rand(10), color=COLORS[2])
        ax3.set_title("Bar Plot with Many Categories")
        ax3.set_xlabel("Categories with Long Names")

        ax4.hist(np.random.normal(0, 1, 100), bins=15, color=COLORS[3], alpha=0.7)
        ax4.set_title("Histogram")
        ax4.set_ylabel("Frequency")

        ax5.plot(x, np.cos(x), color=COLORS[0], label="cos(x)")
        ax5.plot(x, np.sin(x), color=COLORS[1], label="sin(x)")
        ax5.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
        ax5.set_title("Plot with External Legend")

        fig.suptitle("Constrained Layout Example")

        self.assertConversionRight(fig)

    def test_gridspec_margins(self):
        fig = plt.figure(figsize=(10, 8))
        gs = gridspec.GridSpec(
            2,
            2,
            figure=fig,
            left=0.2,  # Left margin
            bottom=0.15,  # Bottom margin
            right=0.8,  # Right margin
            top=0.85,  # Top margin
            wspace=0.3,
            hspace=0.4,
        )

        # Create subplots with custom margins
        for i in range(4):
            ax = fig.add_subplot(gs[i // 2, i % 2])
            x = np.linspace(0, 2 * np.pi, 50)
            y = np.sin(x * (i + 1))
            ax.plot(x, y, color=COLORS[i % len(COLORS)])
            ax.set_title(f"Plot {i + 1}")
            ax.grid(True, alpha=0.3)

        fig.suptitle("GridSpec with Custom Margins")

        self.assertConversionRight(fig)

    def test_gridspec_figure_positioning(self):
        # Test different figure positioning parameters
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))

        # Test 1: Default positioning
        gs1 = gridspec.GridSpec(
            2, 1, figure=fig, left=0.05, right=0.25, top=0.9, bottom=0.1
        )
        ax1a = fig.add_subplot(gs1[0, 0])
        ax1b = fig.add_subplot(gs1[1, 0])

        x, y = get_data()
        ax1a.plot(x, y, color=COLORS[0])
        ax1a.set_title("Left Column - Top")
        ax1b.scatter(x[::5], y[::5], color=COLORS[1])
        ax1b.set_title("Left Column - Bottom")

        # Test 2: Center positioning
        gs2 = gridspec.GridSpec(
            2, 1, figure=fig, left=0.35, right=0.65, top=0.9, bottom=0.1
        )
        ax2a = fig.add_subplot(gs2[0, 0])
        ax2b = fig.add_subplot(gs2[1, 0])

        ax2a.bar(range(5), [1, 3, 2, 4, 2], color=COLORS[2])
        ax2a.set_title("Center Column - Top")
        ax2b.hist(np.random.normal(0, 1, 100), bins=15, alpha=0.7, color=COLORS[3])
        ax2b.set_title("Center Column - Bottom")

        # Test 3: Right positioning
        gs3 = gridspec.GridSpec(
            2, 1, figure=fig, left=0.75, right=0.95, top=0.9, bottom=0.1
        )
        ax3a = fig.add_subplot(gs3[0, 0])
        ax3b = fig.add_subplot(gs3[1, 0])

        theta = np.linspace(0, 2 * np.pi, 100)
        ax3a.plot(theta, np.cos(theta), color=COLORS[0])
        ax3a.set_title("Right Column - Top")
        ax3b.step(theta[:20], np.sin(theta[:20]), color=COLORS[1])
        ax3b.set_title("Right Column - Bottom")

        fig.suptitle("GridSpec Figure Positioning (left, right, top, bottom)")

        self.assertConversionRight(fig)

    def test_gridspec_complex_spacing(self):
        fig = plt.figure(figsize=(12, 10))

        # Create multiple GridSpecs with different spacing parameters
        gs_top = gridspec.GridSpec(
            1,
            3,
            figure=fig,
            left=0.1,
            right=0.9,
            top=0.95,
            bottom=0.7,
            wspace=0.1,  # Tight horizontal spacing
        )

        gs_middle = gridspec.GridSpec(
            2,
            2,
            figure=fig,
            left=0.1,
            right=0.9,
            top=0.65,
            bottom=0.35,
            wspace=0.4,
            hspace=0.2,  # Different spacing
        )

        gs_bottom = gridspec.GridSpec(
            1, 1, figure=fig, left=0.2, right=0.8, top=0.3, bottom=0.05
        )

        # Fill top row
        for i in range(3):
            ax = fig.add_subplot(gs_top[0, i])
            x = np.linspace(0, 2 * np.pi, 50)
            y = np.sin(x + i * np.pi / 2)
            ax.plot(x, y, color=COLORS[i])
            ax.set_title(f"Top {i + 1}")

        # Fill middle grid
        for i in range(4):
            ax = fig.add_subplot(gs_middle[i // 2, i % 2])
            data = np.random.rand(20) + i * 0.5
            ax.bar(range(len(data)), data, color=COLORS[i % len(COLORS)], alpha=0.7)
            ax.set_title(f"Middle {i + 1}")

        # Fill bottom
        ax_bottom = fig.add_subplot(gs_bottom[0, 0])
        x = np.linspace(0, 10, 100)
        y = np.exp(-x / 5) * np.sin(x)
        ax_bottom.plot(x, y, color=COLORS[0], linewidth=2)
        ax_bottom.set_title("Bottom - Spanning")

        fig.suptitle("Complex GridSpec Spacing", y=0.98)

        self.assertConversionRight(fig)

    def test_gridspec_unequal_spacing(self):
        fig = plt.figure(figsize=(12, 8))

        # Create GridSpec with unequal spacing and custom margins
        gs = gridspec.GridSpec(
            3,
            4,
            figure=fig,
            left=0.08,
            right=0.92,
            top=0.92,
            bottom=0.08,
            width_ratios=[1, 2, 1, 3],  # Unequal column widths
            height_ratios=[1, 3, 2],  # Unequal row heights
            wspace=0.3,
            hspace=0.4,
        )

        # Create subplots spanning different areas
        ax1 = fig.add_subplot(gs[0, :2])  # Top left, spanning 2 columns
        ax2 = fig.add_subplot(gs[0, 2:])  # Top right, spanning 2 columns
        ax3 = fig.add_subplot(gs[1, 0])  # Middle left
        ax4 = fig.add_subplot(gs[1, 1:3])  # Middle center, spanning 2 columns
        ax5 = fig.add_subplot(gs[1, 3])  # Middle right
        ax6 = fig.add_subplot(gs[2, :])  # Bottom, spanning all columns

        # Plot different types of data
        x, y = get_data()

        ax1.plot(x, y, color=COLORS[0])
        ax1.set_title("Top Left")

        ax2.scatter(x[::5], y[::5], color=COLORS[1], alpha=0.6)
        ax2.set_title("Top Right")

        ax3.pie([1, 2, 3], colors=COLORS[:3], autopct="%1.1f%%")
        ax3.set_title("Middle Left")

        # 2D plot
        X, Y = np.meshgrid(np.linspace(0, 1, 20), np.linspace(0, 1, 20))
        Z = np.sin(2 * np.pi * X) * np.cos(2 * np.pi * Y)
        im = ax4.imshow(Z, cmap="viridis", extent=[0, 1, 0, 1])
        ax4.set_title("Middle Center")

        ax5.bar(range(5), [1, 3, 2, 5, 4], color=COLORS[2])
        ax5.set_title("Middle Right")

        # Multiple lines in bottom
        for i in range(3):
            y_line = np.sin(x + i * np.pi / 3)
            ax6.plot(x, y_line, color=COLORS[i], label=f"Line {i + 1}")
        ax6.legend()
        ax6.set_title("Bottom - Full Width")

        fig.suptitle("GridSpec with Unequal Spacing and Custom Ratios")

        self.assertConversionRight(fig)

    def test_gridspec_figure_fractions(self):
        fig = plt.figure(figsize=(10, 8))

        # Test precise figure fraction control
        gs_quarter1 = gridspec.GridSpec(
            1, 1, figure=fig, left=0.05, right=0.45, top=0.9, bottom=0.55
        )

        gs_quarter2 = gridspec.GridSpec(
            1, 1, figure=fig, left=0.55, right=0.95, top=0.9, bottom=0.55
        )

        gs_quarter3 = gridspec.GridSpec(
            1, 1, figure=fig, left=0.05, right=0.45, top=0.45, bottom=0.1
        )

        gs_quarter4 = gridspec.GridSpec(
            1, 1, figure=fig, left=0.55, right=0.95, top=0.45, bottom=0.1
        )

        # Create four separate plots
        ax1 = fig.add_subplot(gs_quarter1[0, 0])
        ax2 = fig.add_subplot(gs_quarter2[0, 0])
        ax3 = fig.add_subplot(gs_quarter3[0, 0])
        ax4 = fig.add_subplot(gs_quarter4[0, 0])

        # Different plot types in each quarter
        x = np.linspace(0, 2 * np.pi, 100)

        # Quarter 1: Line plot
        ax1.plot(x, np.sin(x), color=COLORS[0], linewidth=2)
        ax1.set_title("Q1: Line Plot")
        ax1.grid(True, alpha=0.3)

        # Quarter 2: Scatter plot
        x_scatter = np.random.rand(50)
        y_scatter = np.random.rand(50)
        ax2.scatter(
            x_scatter, y_scatter, c=np.random.rand(50), cmap="viridis", s=60, alpha=0.7
        )
        ax2.set_title("Q2: Scatter Plot")

        # Quarter 3: Bar plot
        categories = ["A", "B", "C", "D", "E"]
        values = [23, 45, 56, 78, 32]
        ax3.bar(categories, values, color=COLORS[1])
        ax3.set_title("Q3: Bar Plot")

        # Quarter 4: Histogram
        data = np.random.normal(0, 1, 1000)
        ax4.hist(data, bins=25, alpha=0.7, color=COLORS[2], edgecolor="black")
        ax4.set_title("Q4: Histogram")

        fig.suptitle("GridSpec Figure Fractions - Precise Control")

        self.assertConversionRight(fig)

    def test_subplot_params(self):
        fig, axes = plt.subplots(2, 2, figsize=(10, 8))

        # Adjust subplot parameters
        plt.subplots_adjust(
            left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4
        )

        # Fill subplots
        for i, ax in enumerate(axes.flat):
            x = np.linspace(0, 2 * np.pi, 50)
            y = np.sin(x * (i + 1))
            ax.plot(x, y, color=COLORS[i])
            ax.set_title(f"sin({i + 1}x)")
            ax.grid(True, alpha=0.3)

        fig.suptitle("Manual Subplot Parameters")

        self.assertConversionRight(fig)
