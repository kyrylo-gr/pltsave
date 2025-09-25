import abc
import inspect
import os
import shutil
import sys

CURRENT_DIR = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(CURRENT_DIR, ".."))

from tests.frontend.plot_1d_test import (  # noqa: E402 # pylint: disable=C0413, E0401, E0611
    ClassicalPlotsTest,
)
from tests.test_utils import DATA_DIR  # noqa: E402 # pylint: disable=C0413


def clean_code(code: str):
    code_lines = []

    for line in code.split("\n"):
        if line.startswith("    "):
            line = line[4:]
        code_lines.append(line)

    while code_lines and code_lines[-1] == "":
        code_lines.pop()

    return "\n".join(code_lines[1:-1])


class KeepFiles:
    @property
    @abc.abstractmethod
    def image_path(self) -> str:
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
        if os.path.exists(str(cls.image_path)):
            shutil.rmtree(str(cls.image_path))
        os.makedirs(str(cls.image_path), exist_ok=True)
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
                os.path.join(str(cls.image_path), f.replace("_fig1", "")),
            )

    @classmethod
    def create_md_file(cls):
        examples_dir = os.path.join(CURRENT_DIR, "examples")
        md = f"# {cls.title}\n"

        with open(os.path.join(examples_dir, "start.md"), "r", encoding="utf-8") as f:
            md += f.read()

        for f in os.listdir(str(cls.image_path)):
            md += f"![{f}]({cls.image_path_rel}/{f})\n"

        with open(os.path.join(examples_dir, str(cls.file_name)), "w", encoding="utf-8") as f:
            f.write(md)

    @classmethod
    def get_tests_code(cls):
        tests_methods = {}
        for method in dir(cls):
            if method.startswith("test_") and callable(getattr(cls, method)):
                tests_methods[method] = clean_code(inspect.getsource(getattr(cls, method)))
        return tests_methods

    @classmethod
    def deploy(cls):
        cls.prepare_dir()
        cls.run_all_tests()  # pylint: disable=no-member # type: ignore
        cls.delete_duplicates()
        cls.copy_files()
        cls.create_md_file()


class ClassicalPlots(KeepFiles, ClassicalPlotsTest):
    image_path = os.path.join(CURRENT_DIR, "images", "plot_1d")  # type: ignore
    image_path_rel = os.path.join("..", "images", "plot_1d")  # type: ignore
    file_name = "plot_1d.md"  # type: ignore
    title = "Testing 1D plots"  # type: ignore


if __name__ == "__main__":
    ClassicalPlots.deploy()
