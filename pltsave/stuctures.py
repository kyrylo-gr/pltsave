from dataclasses import asdict, dataclass
import matplotlib as mpl
import numpy as np


@dataclass
class ArtistInfo:
    _children = None

    @property
    def children(self):
        if self._children is None:
            self._children = []
        return self._children

    def params(self):
        return asdict(self)

    def dict(self):
        d = self.params()
        d['children'] = [
            (child.dict() if hasattr(child, 'dict') else child)
            for child in self.children]
        d['__name__'] = self.__class__.__name__
        return d

    def __str__(self) -> str:
        return str(self.dict())


@dataclass
class LineInfo(ArtistInfo):
    xdata: np.ndarray
    ydata: np.ndarray
    color: str = "black"
    alpha: int = 1
    ls: str = "-"
    lw: int = 1.5
    ds: str = "default"
    marker: str = "None"
    label: str = ""
    _elm = mpl.lines.Line2D
    _func = "add_line"

    @staticmethod
    def from_mpl(elm: mpl.lines.Line2D):
        return LineInfo(
            *elm.get_data(),
            color=elm.get_color(),
            alpha=elm.get_alpha(),
            ls=elm.get_ls(),
            lw=elm.get_lw(),
            ds=elm.get_ds(),
            marker=elm.get_marker(),
            label=elm.get_label(),
        )


@dataclass
class AxesInfo(ArtistInfo):
    xlim: tuple = (0, 1)
    ylim: tuple = (0, 1)
    rect: tuple = (0, 0, 1, 1)

    @staticmethod
    def from_mpl(elm: mpl.lines.Line2D):
        return AxesInfo(
            xlim=elm.get_xlim(),
            ylim=elm.get_ylim(),
            rect=elm.get_position().bounds
        )


@dataclass
class LegendInfo(ArtistInfo):
    loc: int

    @staticmethod
    def from_mpl(elm: mpl.lines.Line2D):
        return LegendInfo(
            loc=elm._get_loc()  # pylint: disable=W0212
        )


@dataclass
class FigureInfo(ArtistInfo):
    @staticmethod
    def from_mpl(elm: mpl.lines.Line2D):
        del elm
        return FigureInfo()
