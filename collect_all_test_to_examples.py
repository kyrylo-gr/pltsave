import os
import sys
import shutil
import abc

CURRENT_DIR = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(CURRENT_DIR, ".."))

from tests.frontend.plot_1d_test import ClassicalPlotsTest  # noqa: E402 # pylint: disable=C0413
from tests.test_utils import DATA_DIR  # noqa: E402 # pylint: disable=C0413


class KeepFiles:
    @property
    @abc.abstractmethod
    def image_path(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def image_path_rel(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def file_name(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def title(self):
        raise NotImplementedError

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    @classmethod
    def prepare_dir(cls):
        if os.path.exists(cls.image_path):
            shutil.rmtree(cls.image_path)
        os.makedirs(cls.image_path, exist_ok=True)
        os.makedirs(os.path.join(CURRENT_DIR, "examples"), exist_ok=True)

    @classmethod
    def delete_duplicates(cls):
        for f in os.listdir(DATA_DIR):
            if f.endswith("2.png"):
                os.remove(os.path.join(DATA_DIR, f))

    @classmethod
    def copy_files(cls):
        for f in os.listdir(DATA_DIR):
            shutil.move(
                os.path.join(DATA_DIR, f),
                os.path.join(cls.image_path, f.replace("_fig1", "")),
            )

    @classmethod
    def create_md_file(cls):
        examples_dir = os.path.join(CURRENT_DIR, "examples")
        md = f"# {cls.title}\n"

        with open(os.path.join(examples_dir, "start.md"), "r", encoding="utf-8") as f:
            md += f.read()

        for f in os.listdir(cls.image_path):
            md += f"![{f}]({cls.image_path_rel}/{f})\n"

        with open(os.path.join(examples_dir, cls.file_name), "w", encoding="utf-8") as f:
            f.write(md)

    @classmethod
    def deploy(cls):
        cls.prepare_dir()
        cls.run_all_tests()  # pylint: disable=no-member
        cls.delete_duplicates()
        cls.copy_files()
        cls.create_md_file()


class ClassicalPlots(KeepFiles, ClassicalPlotsTest):
    image_path = os.path.join(CURRENT_DIR, "images", "plot_1d")
    image_path_rel = os.path.join("..", "images", "plot_1d")
    file_name = "plot_1d.md"
    title = "Testing 1D plots"


ClassicalPlots.deploy()
