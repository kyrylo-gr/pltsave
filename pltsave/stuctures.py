from dataclasses import asdict, dataclass
from typing import List, Literal, Optional
from matplotlib import axes, lines, collections, axis, text as mtext
import numpy as np
import json
from . import json_coders


@dataclass
class ArtistInfo:
    _children = None
    _transformation = None

    @property
    def children(self) -> List["ArtistInfo"]:
        if self._children is None:
            self._children = []
        return self._children

    @property
    def transformation(self) -> "TransformationInfo":
        return self._transformation

    @transformation.setter
    def transformation(self, value):
        self._transformation = value

    def params(self):
        data = asdict(self)
        for k, v in list(data.items()):
            if v is None:
                data.pop(k)
        return data

    def to_dict(self):
        d = self.params()
        d["children"] = [
            (child.to_dict() if hasattr(child, "to_dict") else child) for child in self.children
        ]
        if self.transformation:
            d["transformation"] = self.transformation.to_dict()
        d["__name__"] = self.__class__.__name__
        return d

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True, indent=4, cls=json_coders.StringEncoder)

    @classmethod
    def from_json(cls, s):
        data = json.loads(s, cls=json_coders.NumbersDecoder)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict) -> "ArtistInfo":
        # return data
        if not isinstance(data, dict):
            print("!!!!", data)

        # print(data)
        if data.get("__name__") not in NAMES_OF_CLASSES:
            return data
        # if 'children' in data:
        children = [cls.from_dict(child) for child in data.pop("children", [])]
        transformation = data.pop("transformation", None)

        # else:
        # children = None

        cls_name = NAMES_OF_CLASSES[data.pop("__name__")]
        data = cls_name(**data)
        if children:
            data._children = children  # pylint: disable=W0212
        if transformation:
            # print(transformation)
            data.transformation = TransformationInfo.from_dict(transformation)

        return data

    def __str__(self) -> str:
        return str(self.to_dict())

    def load_to(self, elm):
        del elm


@dataclass
class TransformationInfo(ArtistInfo):
    which: Optional[str] = None

    @staticmethod
    def dumps_from_obj(elm: lines.Line2D):
        if hasattr(elm, "_axes"):
            if elm.get_transform() is elm._axes.get_xaxis_transform(which="grid"):
                return TransformationInfo(which="x_grid")
            if elm.get_transform() is elm._axes.get_yaxis_transform(which="grid"):
                return TransformationInfo(which="y_grid")

    def load_to(self, elm: lines.Line2D):
        if self.which == "x_grid":
            elm.set_transform(elm._axes.get_xaxis_transform(which="grid"))
        if self.which == "y_grid":
            elm.set_transform(elm._axes.get_yaxis_transform(which="grid"))


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
    markerfacecolor: Optional[str] = None
    markeredgecolor: Optional[str] = None
    label: str = ""
    zorder: Optional[int] = None

    _elm = lines.Line2D
    _func = "add_line"

    @staticmethod
    def dumps(elm: lines.Line2D):
        return LineInfo(
            *elm.get_data(),
            color=elm.get_color(),
            alpha=elm.get_alpha(),
            ls=elm.get_ls(),
            lw=elm.get_lw(),
            ds=elm.get_ds(),
            marker=elm.get_marker(),
            markerfacecolor=elm.get_markerfacecolor(),
            markeredgecolor=elm.get_markeredgecolor(),
            label=elm.get_label(),
            zorder=elm.get_zorder(),
        )

    def load_to(self, ax: axes.Axes):
        line = self._elm(**self.params())  # pylint: disable=W0212
        getattr(ax, self._func)(line)
        if self.transformation:
            self.transformation.load_to(line)


@dataclass
class LineCollectionInfo(ArtistInfo):
    segments: List[List[float]]

    color: Optional[str] = None
    alpha: Optional[int] = 1
    ls: Optional[str] = None
    lw: Optional[int] = None

    label: Optional[str] = None
    zorder: Optional[int] = None

    _elm = collections.LineCollection
    _func = "add_collection"

    @staticmethod
    def dumps(elm: collections.LineCollection):
        return LineCollectionInfo(
            segments=elm.get_segments(),
            color=elm.get_color(),
            alpha=elm.get_alpha(),
            # ls=elm.get_ls(),
            # lw=elm.get_lw(),
            label=elm.get_label(),
            zorder=elm.get_zorder(),
        )

    def load_to(self, ax: axes.Axes):
        line = self._elm(**self.params())  # pylint: disable=W0212
        getattr(ax, self._func)(line)
        if self.transformation:
            self.transformation.load_to(line)


@dataclass
class AxesInfo(ArtistInfo):
    xlim: tuple = (0, 1)
    ylim: tuple = (0, 1)
    rect: tuple = (0, 0, 1, 1)
    xlabel: str = None
    ylabel: str = None
    title: str = None
    xticks: list = None
    yticks: list = None

    @staticmethod
    def dumps(elm: lines.Line2D):
        return AxesInfo(
            xlim=elm.get_xlim(),
            ylim=elm.get_ylim(),
            rect=elm.get_position().bounds,
            xlabel=elm.get_xlabel(),
            ylabel=elm.get_ylabel(),
            title=elm.get_title(),
            # xticks=elm.get_xticks(),
            # yticks=elm.get_yticks(),
        )


@dataclass
class LegendInfo(ArtistInfo):
    loc: int

    @staticmethod
    def dumps(elm: lines.Line2D):
        return LegendInfo(loc=elm._get_loc())  # pylint: disable=W0212

    def load_to(self, ax: axes.Axes):
        ax.legend(loc=self.loc)


@dataclass
class FigureInfo(ArtistInfo):
    @staticmethod
    def dumps(elm: lines.Line2D):
        del elm
        return FigureInfo()


@dataclass
class AxisInfo(ArtistInfo):
    direction: Literal["x", "y"]
    left: bool = True
    right: bool = False
    labelleft: bool = True
    labelright: bool = False
    gridOn: bool = False

    @classmethod
    def dumps(cls, elm: axis.Axis):
        return cls(**elm.get_tick_params())

    def load_to(self, ax: axes.Axes):
        if self.gridOn:
            ax.grid(axis=self.direction)


@dataclass
class XAxisInfo(AxisInfo):
    direction: str = "x"


@dataclass
class YAxisInfo(AxisInfo):
    direction: str = "y"


@dataclass
class AnnotationInfo(ArtistInfo):
    text: str
    xy: tuple
    xytext: tuple
    xycoords: str = "data"
    arrowprops: Optional[dict] = None

    @classmethod
    def dumps(cls, elm: mtext.Annotation):
        text = elm._text  # pylint: disable=W0212

        return cls(
            text=text,
            xy=elm.xy,
            xytext=(elm._x, elm._y),  # pylint: disable=W0212
            xycoords=elm.xycoords,
            arrowprops=elm.arrowprops,
        )

    def load_to(self, ax: axes.Axes):
        text = mtext.Annotation(**self.params())
        ax._add_text(text)  # pylint: disable=W0212


NAMES_OF_CLASSES = {
    "LineInfo": LineInfo,
    "AxesInfo": AxesInfo,
    "LegendInfo": LegendInfo,
    "FigureInfo": FigureInfo,
    "LineCollectionInfo": LineCollectionInfo,
    "TransformationInfo": TransformationInfo,
    "XAxisInfo": XAxisInfo,
    "YAxisInfo": YAxisInfo,
    "AnnotationInfo": AnnotationInfo,
}
