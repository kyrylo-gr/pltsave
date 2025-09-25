import json
from dataclasses import asdict, dataclass
from typing import Dict, List, Literal, Optional, Type, Union

import numpy as np
from matplotlib import axes, axis, collections, figure, image, legend, lines
from matplotlib import text as mtext

from . import json_coders
from .aliases import SHORT_NAMES_OF_CLASSES, SHORT_NAMES_OF_CLASSES_INVERSE
from .compress.routines import decode_dict, encode_dict
from .defaults import DEFAULT_COLORS, DEFAULT_COLORS_REVERSE, DEFAULT_VALUES

# from matplotlib.artist import Artist


def dict_filter_non_none(d: dict, keys: Optional[List[str]] = None) -> dict:
    ks = keys or d.keys()
    return {k: d[k] for k in ks if d[k] is not None}


def kwargs_filter_non_none(elm, keys):
    res = {}
    for key in keys:
        if hasattr(elm, key):
            val = getattr(elm, key)
            if val is not None:
                res[key] = val
    return res


def kwargs_filter_default(elm, keys):
    kwargs = {}
    for key in keys:
        if key == "color":
            kwargs["color"] = check_default_color(str(elm.get_color()))
            continue
        if key == "label":
            label = elm.get_label()
            if label and label[0] != "_":
                kwargs["label"] = label
            continue

        value = getattr(elm, f"get_{key}")()
        if (key not in DEFAULT_VALUES or value != DEFAULT_VALUES[key]) and value is not None:
            kwargs[key] = value

    return kwargs


def check_default_color(color: str):
    return DEFAULT_COLORS_REVERSE.get(color, color)


def get_default_color(color: Union[str, int]):
    if isinstance(color, int) or (isinstance(color, str) and color.isdigit()):
        return DEFAULT_COLORS.get(int(color), color)
    return color


@dataclass
class ArtistInfo:
    _children = None
    _transformation = None
    _elm = None  # type: ignore

    @property
    def children(self) -> List["ArtistInfo"]:
        if self._children is None:
            self._children = []
        return self._children

    @property
    def transformation(self) -> "Optional[TransformationInfo]":
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
        d = dict_filter_non_none(self.params())
        children = [
            (child.to_dict() if hasattr(child, "to_dict") else child) for child in self.children
        ]
        if children:
            d["children"] = children
        if self.transformation:
            d["transformation"] = self.transformation.to_dict()
        d["__name__"] = SHORT_NAMES_OF_CLASSES[self.__class__.__name__]
        return d

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True, indent=4, cls=json_coders.StringEncoder)

    def to_compresed_str(self):
        return encode_dict(self.to_dict())

    def to_url(self, title: Optional[str] = None):
        if title:
            return f"[{title}]({self.to_url()})"
        return f"//papir.app/pl?t={self.to_compresed_str()}"

    @classmethod
    def from_json(cls, s):
        data = json.loads(s, cls=json_coders.NumbersDecoder)
        return cls.from_dict(data)

    @classmethod
    def from_compresed_str(cls, s):
        data = decode_dict(s)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict) -> "ArtistInfo":
        if not isinstance(data, dict):
            raise ValueError(f"Expected dict, got {type(data)}")

        class_name = data.pop("__name__")
        class_name = SHORT_NAMES_OF_CLASSES_INVERSE.get(class_name, class_name)

        if class_name not in NAMES_OF_CLASSES:
            raise ValueError(f"Unknown class name: {class_name}")

        children = [cls.from_dict(child) for child in data.pop("children", [])]
        transformation = data.pop("transformation", None)

        cls_type = NAMES_OF_CLASSES[class_name]

        obj = cls_type(**data)
        if children:
            obj._children = children  # pylint: disable=W0212
        if transformation:
            obj.transformation = TransformationInfo.from_dict(transformation)

        return obj

    def __str__(self) -> str:
        return str(self.__class__.__name__)

    def __repr__(self) -> str:
        return self.__str__()

    def load_to(self, elm, /):
        del elm

    def loads(self, /, **kwargs):
        raise NotImplementedError


@dataclass
class TransformationInfo(ArtistInfo):
    which: Optional[str] = None

    @staticmethod
    def dumps_from_obj(elm: lines.Line2D):
        if hasattr(elm, "_axes"):
            if (
                elm.get_transform()
                is elm._axes.get_xaxis_transform(  # pylint: disable=W0212 # type: ignore
                    which="grid"
                )
            ):
                return TransformationInfo(which="x_grid")
            if (
                elm.get_transform()
                is elm._axes.get_yaxis_transform(  # pylint: disable=W0212 # type: ignore
                    which="grid"
                )
            ):
                return TransformationInfo(which="y_grid")

    def load_to(self, elm: Union[lines.Line2D, collections.LineCollection], /):
        if self.which == "x_grid":
            elm.set_transform(
                elm._axes.get_xaxis_transform(which="grid")  # pylint: disable=W0212 # type: ignore
            )  # pylint: disable=W0212 # type: ignore
        if self.which == "y_grid":
            elm.set_transform(
                elm._axes.get_yaxis_transform(which="grid")  # pylint: disable=W0212 # type: ignore
            )  # pylint: disable=W0212 # type: ignore


@dataclass
class LineInfo(ArtistInfo):
    xdata: np.ndarray
    ydata: np.ndarray
    color: Optional[str] = None
    alpha: Optional[float] = None
    linestyle: Optional[str] = None
    linewidth: Optional[float] = None
    drawstyle: Optional[str] = None
    marker: Optional[Union[str, int]] = None
    markerfacecolor: Optional[str] = None
    markeredgecolor: Optional[str] = None
    label: Optional[str] = None
    zorder: Optional[int] = None

    _elm = lines.Line2D
    _func = "add_line"

    @staticmethod
    def dumps(elm: lines.Line2D):
        kwargs = kwargs_filter_default(
            elm,
            [
                "alpha",
                "linestyle",
                "linewidth",
                "drawstyle",
                "marker",
                "color",
                "label",
            ],
        )
        if kwargs.get("marker", "None") != "None":
            kwargs["markerfacecolor"] = check_default_color(str(elm.get_markerfacecolor()))
            kwargs["markeredgecolor"] = check_default_color(str(elm.get_markeredgecolor()))

        return LineInfo(
            *elm.get_data(),  # type: ignore
            zorder=elm.get_zorder(),
            **kwargs,
        )

    def load_to(self, ax: axes.Axes, /):
        pass
        # params = self.params()
        # if "color" in params:
        #     params["color"] = get_default_color(params["color"])

        # line = lines.Line2D(**params)  # pylint: disable=W0212
        # getattr(ax, self._func)(line)
        # if self.transformation:
        #     self.transformation.load_to(line)

    def loads(self, /, **kwargs):
        ax: axes.Axes = kwargs["ax"]
        params = self.params()
        if "color" in params:
            params["color"] = get_default_color(params["color"])
        if "markeredgecolor" in params:
            params["markeredgecolor"] = get_default_color(params["markeredgecolor"])
        if "markerfacecolor" in params:
            params["markerfacecolor"] = get_default_color(params["markerfacecolor"])
        line = lines.Line2D(**params)
        ax.add_line(line)
        if self.transformation:
            self.transformation.load_to(line)

        return line


@dataclass
class LineCollectionInfo(ArtistInfo):
    segments: List[List[float]]

    color: Optional[str] = None
    alpha: Optional[int] = None
    linestyle: Optional[str] = None
    linewidth: Optional[int] = None

    label: Optional[str] = None
    zorder: Optional[int] = None

    _elm = collections.LineCollection
    _func = "add_collection"

    @staticmethod
    def dumps(elm: collections.LineCollection):
        kwargs = kwargs_filter_default(
            elm,
            [
                "color",
                "alpha",
                "linestyle",
                "linewidth",
                "label",
                "zorder",
            ],
        )

        return LineCollectionInfo(
            segments=elm.get_segments(),
            **kwargs,
        )

    def load_to(self, ax: axes.Axes, /):
        pass

    def loads(self, /, **kwargs):
        ax: axes.Axes = kwargs["ax"]
        params = self.params()
        if "color" in params:
            params["color"] = get_default_color(params["color"])

        line = collections.LineCollection(**params)  # pylint: disable=W0212
        ax.add_collection([line])
        if self.transformation:
            self.transformation.load_to(line)


@dataclass
class AxesInfo(ArtistInfo):
    xlim: tuple = (0, 1)
    ylim: tuple = (0, 1)
    rect: tuple = (0, 0, 1, 1)
    xlabel: Optional[str] = None
    ylabel: Optional[str] = None
    title: Optional[str] = None
    xticks: Optional[list] = None
    yticks: Optional[list] = None

    _elm = axes.Axes

    @staticmethod
    def dumps(elm: axes.Axes):

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

    def load_to(self, ax: axes.Axes, /):
        pass

    def loads(self, /, **kwargs):
        fig: figure.Figure = kwargs["fig"]
        ax = axes.Axes(fig=fig, **self.params())

        for child in self.children:
            child.loads(ax=ax, **kwargs)
        fig.add_axes(ax)
        return ax


@dataclass
class LegendInfo(ArtistInfo):
    loc: int

    @staticmethod
    def dumps(elm: legend.Legend):
        return LegendInfo(loc=elm._get_loc())  # pylint: disable=W0212 # type: ignore

    def load_to(self, ax: axes.Axes, /):
        ax.legend(loc=self.loc)

    def loads(self, /, **kwargs):
        obj = kwargs.get("ax", kwargs["fig"])
        obj.legend(loc=self.loc)


@dataclass
class FigureInfo(ArtistInfo):
    _elm = figure.Figure

    @staticmethod
    def dumps(elm: figure.Figure):
        del elm
        return FigureInfo()

    def load(self, fig: figure.Figure, /, **kwargs):
        for child in self.children:
            child.loads(fig=fig, **kwargs)

    def loads(self, /, **kwargs):
        fig = figure.Figure()
        self.load(fig, **kwargs)
        return fig


@dataclass
class AxisInfo(ArtistInfo):
    direction: Literal["x", "y"]
    left: bool = True
    right: bool = False
    labelleft: bool = True
    labelright: bool = False
    gridOn: bool = False

    _elm = axis.Axis

    @classmethod
    def dumps(cls, elm: axis.Axis):
        return cls(**elm.get_tick_params())  # type: ignore

    def load_to(self, ax: axes.Axes, /):
        if self.gridOn:
            ax.grid(axis=self.direction)


@dataclass
class XAxisInfo(AxisInfo):
    direction = "x"


@dataclass
class YAxisInfo(AxisInfo):
    direction = "y"


@dataclass
class AnnotationInfo(ArtistInfo):
    text: str
    xy: tuple
    xytext: tuple
    xycoords: str = "data"
    arrowprops: Optional[dict] = None

    @classmethod
    def dumps(cls, elm: mtext.Annotation):
        text = elm._text  # pylint: disable=W0212 # type: ignore

        return cls(
            text=text,
            xy=elm.xy,  # type: ignore
            xytext=(elm._x, elm._y),  # pylint: disable=W0212 # type: ignore
            xycoords=elm.xycoords,  # type: ignore
            arrowprops=elm.arrowprops,  # type: ignore
        )

    def load_to(self, ax: axes.Axes, /):
        text = mtext.Annotation(**self.params())
        ax._add_text(text)  # pylint: disable=W0212 # type: ignore


@dataclass
class AxesImageInfo(ArtistInfo):
    data: np.ndarray
    aspect: float = 1.0
    extent: Optional[list] = None
    origin: str = "upper"
    cmap: Optional[str] = None

    @classmethod
    def dumps(cls, elm: image.AxesImage):
        colormap = elm.get_cmap()
        if colormap is not None:
            if hasattr(colormap, "name"):
                colormap = colormap.name  # type: ignore
            else:
                colormap = None  # TODO: add support for custom colormaps
        return cls(
            data=elm.get_array().data,
            aspect=elm._axes._aspect,  # pylint: disable=W0212 # type: ignore
            extent=elm.get_extent(),  # type: ignore
            origin=elm.origin,  # type: ignore
            cmap=colormap,
        )

    def load_to(self, ax: axes.Axes, /):
        kwargs = kwargs_filter_non_none(self, ["aspect", "extent", "origin", "cmap"])
        ax.imshow(np.array(self.data), **kwargs)


NAMES_OF_CLASSES: Dict[str, Type[ArtistInfo]] = {
    "LineInfo": LineInfo,
    "AxesInfo": AxesInfo,
    "LegendInfo": LegendInfo,
    "FigureInfo": FigureInfo,
    "LineCollectionInfo": LineCollectionInfo,
    "TransformationInfo": TransformationInfo,
    "XAxisInfo": XAxisInfo,
    "YAxisInfo": YAxisInfo,
    "AnnotationInfo": AnnotationInfo,
    "AxesImageInfo": AxesImageInfo,
}
