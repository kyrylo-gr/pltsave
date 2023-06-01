from dataclasses import asdict, dataclass
import matplotlib as mpl
import numpy as np
import json
from . import json_coders


@dataclass
class ArtistInfo:
    _children = None

    @property
    def children(self):
        if self._children is None:
            self._children = []
        return self._children

    def params(self):
        data = asdict(self)
        for k, v in list(data.items()):
            if v is None:
                data.pop(k)
        return data

    def to_dict(self):
        d = self.params()
        d['children'] = [
            (child.to_dict() if hasattr(child, 'to_dict') else child)
            for child in self.children]
        d['__name__'] = self.__class__.__name__
        return d

    def to_json(self):
        return json.dumps(
            self.to_dict(),
            sort_keys=True,
            indent=4,
            cls=json_coders.StringEncoder)

    @classmethod
    def from_json(cls, s):
        data = json.loads(
            s, cls=json_coders.NumbersDecoder)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict):
        # return data
        if not isinstance(data, dict):
            pass
        if data.get('__name__', None) not in NAMES_OF_CLASSES:
            return data
        # if 'children' in data:
        children = [cls.from_dict(child)
                    for child in data.pop('children', [])]
        # else:
        # children = None

        cls_name = NAMES_OF_CLASSES[data.pop('__name__')]
        data = cls_name(**data)
        if children:
            data._children = children  # pylint: disable=W0212

        return data

    def __str__(self) -> str:
        return str(self.to_dict())


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
    xlabel: str = None
    ylabel: str = None
    xticks: list = None
    yticks: list = None

    @staticmethod
    def from_mpl(elm: mpl.lines.Line2D):
        return AxesInfo(
            xlim=elm.get_xlim(),
            ylim=elm.get_ylim(),
            rect=elm.get_position().bounds,
            xlabel=elm.get_xlabel(),
            ylabel=elm.get_ylabel(),
            # xticks=elm.get_xticks(),
            # yticks=elm.get_yticks(),
        )


@dataclass
class LegendInfo(ArtistInfo):
    loc: int

    @staticmethod
    def from_mpl(elm: mpl.lines.Line2D):
        return LegendInfo(
            loc=elm._get_loc()  # pylint: disable=W0212
        )


# @dataclass
# class AxisInfo(ArtistInfo):
#     label: str

#     @staticmethod
#     def from_mpl(elm: mpl.lines.Line2D):
#         return AxisInfo(
#             label=elm.get_label()
#         )


@dataclass
class FigureInfo(ArtistInfo):
    @staticmethod
    def from_mpl(elm: mpl.lines.Line2D):
        del elm
        return FigureInfo()


NAMES_OF_CLASSES = {
    'LineInfo': LineInfo,
    'AxesInfo': AxesInfo,
    'LegendInfo': LegendInfo,
    'FigureInfo': FigureInfo
}
