import unittest
import os
import shutil
import numpy as np
import matplotlib.pyplot as plt

import pltsave
from .compare_images import images_are_similar

TEST_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(TEST_DIR, "tmp_test_data")

COLORS = ["#0066cc", "#ffcc00", "#ff7400", "#962fbf"]


class BaseTest(unittest.TestCase):
    def setUp(self):
        # if not os.path.exists(DATA_DIR):
        # shutil.rmtree(DATA_DIR)
        os.makedirs(DATA_DIR, exist_ok=True)

    def assertConversionRight(self, fig: 'plt.Figure'):
        info = pltsave.dumps(fig)
        fig2 = pltsave.loads(info)
        self.assertFigEqual(fig, fig2)

    def assertFigEqual(self, fig1: 'plt.Figure', fig2: 'plt.Figure'):
        self._assertFigEqual(fig1, fig2, True)

    def assertFigNotEqual(self, fig1: 'plt.Figure', fig2: 'plt.Figure'):
        self._assertFigEqual(fig1, fig2, False)

    def _assertFigEqual(
        self,
        fig1: 'plt.Figure',
        fig2: 'plt.Figure',
        assert_to: bool,
    ):
        path1 = os.path.join(DATA_DIR, f"{self._testMethodName}_fig1.png")
        path2 = os.path.join(DATA_DIR, f"{self._testMethodName}_fig2.png")
        fig1.savefig(path1)
        fig2.savefig(path2)

        return self.assertImageEqual(path1, path2, assert_to)

    def assertImageEqual(self, path1: str, path2: str, assert_to: bool):
        if assert_to:
            self.assertTrue(images_are_similar(path1, path2))
        else:
            self.assertFalse(images_are_similar(path1, path2))

    def run(self, result=None):
        testMethod = getattr(self, self._testMethodName)

        self.setUp()
        testMethod()
        # it will not run tearDown if there is an error in the test method.
        self.tearDown()

    def tearDown(self):
        path1 = os.path.join(DATA_DIR, f"{self._testMethodName}_fig1.png")
        path2 = os.path.join(DATA_DIR, f"{self._testMethodName}_fig2.png")
        if os.path.exists(path1):
            os.remove(path1)
        if os.path.exists(path2):
            os.remove(path2)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(DATA_DIR) and not os.listdir(DATA_DIR):
            shutil.rmtree(DATA_DIR)


def create_simple_plot(**kwargs):
    fig, ax = plt.subplots(1, 1)
    x = np.linspace(0, 2 * np.pi, 100)
    ax.plot(x, np.sin(x))
    if kwargs:
        ax.set(**kwargs)
    return fig, ax


def plot_on_axis(ax: plt.Axes, **kwargs):
    x, y = get_data()
    ax.plot(x, y)
    if kwargs:
        ax.set(**kwargs)
    return ax


def get_data(length: int = 100):
    x = np.linspace(0, 2 * np.pi, length)
    y = np.sin(x)*np.random.rand(len(x))
    return x, y
