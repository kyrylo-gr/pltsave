import numpy as np
import matplotlib.pyplot as plt

from ..test_utils import BaseTest, COLORS, get_data


class ImshowTest(BaseTest):
    def test_simple_imshow(self):
        t = np.linspace(0, 2 * np.pi, 1024)
        data2d = np.sin(t)[:, np.newaxis] * np.cos(t)[np.newaxis, :]

        fig, ax = plt.subplots()
        ax.imshow(data2d)
        ax.set_title("Some title")

        self.assertConversionRight(fig)

    def test_simple_imshow_extent(self):
        t = np.linspace(0, 2 * np.pi, 1024)
        data2d = np.sin(t)[:, np.newaxis] * np.cos(t)[np.newaxis, :]

        fig, ax = plt.subplots()
        ax.imshow(data2d, extent=[0, 1, 0, 1])
        ax.set_title("Some title")

        self.assertConversionRight(fig)

    def test_simple_imshow_aspect(self):
        pass

    def test_simple_imshow_origin_lower(self):
        t = np.linspace(0, 2 * np.pi, 1024)
        data2d = np.sin(t)[:, np.newaxis] * np.cos(t)[np.newaxis, :]

        fig, ax = plt.subplots()
        ax.imshow(data2d, origin="lower")
        ax.set_title("Some title")

        self.assertConversionRight(fig)

    def test_simple_imshow_origin_upper(self):
        t = np.linspace(0, 2 * np.pi, 1024)
        data2d = np.sin(t)[:, np.newaxis] * np.cos(t)[np.newaxis, :]

        fig, ax = plt.subplots()
        ax.imshow(data2d, origin="upper")
        ax.set_title("Some title")

        self.assertConversionRight(fig)

    def test_simple_imshow_cmap(self):
        t = np.linspace(0, 2 * np.pi, 1024)
        data2d = np.sin(t)[:, np.newaxis] * np.cos(t)[np.newaxis, :]

        fig, ax = plt.subplots()
        ax.imshow(data2d, origin="lower", cmap="PuRd", extent=[0, 1, 0, 1])
        ax.set_title("Some title")

        self.assertConversionRight(fig)

    def test_simple_imshow_colorbar(self):
        t = np.linspace(0, 2 * np.pi, 1024)
        data2d = np.sin(t)[:, np.newaxis] * np.cos(t)[np.newaxis, :]

        fig, ax = plt.subplots()
        im = ax.imshow(data2d, origin="lower")
        ax.set_title("Some title")

        fig.colorbar(im, ax=ax, label="Power")

        self.assertConversionRight(fig)
