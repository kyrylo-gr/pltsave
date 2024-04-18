"""Import pltsave."""

import setuptools

NAME = "pltsave"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def get_version() -> str:
    with open(f"{NAME}/__config__.py", "r", encoding="utf-8") as file:
        for line in file.readlines():
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
    raise ValueError("Version not found")


setuptools.setup(
    name=NAME,
    version=get_version(),
    author="kyrylo",
    author_email="cryo.paris.su@gmail.com",
    description="Data management library to save data and plots to hdf5 files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kyrylo-gr/pltsave",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy",
    ],
    extras_require={
        "dev": [
            "pytest",
        ]
    },
)
