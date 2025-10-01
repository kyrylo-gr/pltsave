import json
from dataclasses import asdict, dataclass
from typing import Dict, List, Literal, Optional, Type, Union

import numpy as np
from matplotlib import (
    axes,
    axis,
    collections,
    container,
    figure,
    image,
    legend,
    lines,
    patches,
    transforms,
)
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
        if (
            key not in DEFAULT_VALUES or value != DEFAULT_VALUES[key]
        ) and value is not None:
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
    # _texts = None
    _transformation = None
    _elm = None  # type: ignore

    @property
    def children(self) -> List["ArtistInfo"]:
        if self._children is None:
            self._children = []
        return self._children

    # @property
    # def texts(self) -> List["ArtistInfo"]:
    #     if self._texts is None:
    #         self._texts = []
    #     return self._texts

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
            (child.to_dict() if hasattr(child, "to_dict") else child)
            for child in self.children
        ]
        if children:
            d["children"] = children
        if self.transformation:
            d["transformation"] = self.transformation.to_dict()
        d["__name__"] = SHORT_NAMES_OF_CLASSES[self.__class__.__name__]
        return d

    def to_json(self):
        return json.dumps(
            self.to_dict(), sort_keys=True, indent=4, cls=json_coders.StringEncoder
        )

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
        raise NotImplementedError(self.__class__.__name__)

    @classmethod
    def dumps(cls, elm, dumps_func, objects_to_exclude: set = set()):
        info = cls._dumps(elm)
        if info is None:
            return None

        for child in elm.get_children():
            if child in objects_to_exclude:
                continue
            child_info = dumps_func(child)  # type: ignore
            if child_info:
                info.children.append(child_info)

        # if hasattr(elm, "texts"):
        # texts = [dumps_func(text) for text in elm.texts]
        # info.texts.extend(texts)

        if hasattr(elm, "get_transform"):
            info.transformation = cls.dumps_transformation(elm)  # type: ignore

        return info

    @classmethod
    def dumps_transformation(cls, elm, **kwargs):
        if hasattr(elm, "get_transform"):
            transformation = elm.get_transform()
            if transformation:
                return TransformationInfo.dumps_from_obj(elm)  # type: ignore
        return None

    @classmethod
    def collect_data(cls, elm, **kwargs):
        return {}

    @classmethod
    def _dumps(cls, elm, **kwargs):
        data = cls.collect_data(elm, **kwargs)
        if data is None:
            return None
        return cls(**data)


@dataclass
class TransformationInfo(ArtistInfo):
    which: Optional[str] = None
    matrix: Optional[np.array] = None

    @classmethod
    def dumps(cls, transform, **kwargs):
        ax: axes.Axes = kwargs.get("ax")
        if ax is None:
            return None

        # raise ValueError("Axes not found")
        if transform == ax.transAxes:
            return TransformationInfo(which="transAxes")
        if transform == ax.transData:
            return TransformationInfo(which="transData")
        if transform == ax.transLimits:
            return TransformationInfo(which="transLimits")
        if transform == ax.transScale:
            return TransformationInfo(which="transScale")
        if isinstance(transform, transforms.CompositeGenericTransform):
            info = TransformationInfo(which="composite")
            info.children.extend(
                (
                    cls.dumps(transform._a, **kwargs),
                    cls.dumps(transform._b, **kwargs),
                )
            )
            return info

        return TransformationInfo(matrix=transform.get_matrix())

    @classmethod
    def dumps_from_obj(cls, elm, **kwargs):
        # if hasattr(elm, "_axes"):
        #     if elm.get_transform() is elm._axes.get_xaxis_transform(  # pylint: disable=W0212 # type: ignore
        #         which="grid"
        #     ):
        #         return TransformationInfo(which="x_grid")
        #     if elm.get_transform() is elm._axes.get_yaxis_transform(  # pylint: disable=W0212 # type: ignore
        #         which="grid"
        #     ):
        #         return TransformationInfo(which="y_grid")
        kwargs["ax"] = getattr(elm, "_axes", kwargs.get("ax"))

        if not hasattr(elm, "get_transform"):
            return None
        transform = elm.get_transform()
        return cls.dumps(transform, **kwargs)

    def loads(self, /, **kwargs):
        if self.matrix is not None:
            return transforms.Affine2D(self.matrix)

        ax: axes.Axes = kwargs.get("ax")
        if ax is None:
            raise ValueError("Axes not found")

        if self.which == "transAxes":
            return ax.transAxes
        if self.which == "transData":
            return ax.transData
        if self.which == "transLimits":
            return ax.transLimits
        if self.which == "transScale":
            return ax.transScale
        if self.which == "composite":
            if len(self.children) != 2:
                raise ValueError(
                    "For the 'composite' transform len(children) should be 2"
                )
            return transforms.CompositeGenericTransform(
                self.children[0].loads(**kwargs),
                self.children[1].loads(**kwargs),
            )

    def load_to(
        self, elm: Union[lines.Line2D, collections.LineCollection], /, **kwargs
    ):
        # if self.which == "x_grid":
        #     elm.set_transform(
        #         elm._axes.get_xaxis_transform(which="grid")  # pylint: disable=W0212 # type: ignore
        #     )  # pylint: disable=W0212 # type: ignore
        # if self.which == "y_grid":
        #     elm.set_transform(
        #         elm._axes.get_yaxis_transform(which="grid")  # pylint: disable=W0212 # type: ignore
        #     )  # pylint: disable=W0212 # type: ignore
        kwargs["ax"]: axes.Axes = kwargs.get("ax", getattr(elm, "_axes"))
        transform = self.loads(**kwargs)

        if transform:
            return elm.set_transform(transform)
        return None


def collect_attributes(elm, attributes, raise_error=True):
    data = {}
    for attr in attributes:
        if hasattr(elm, attr):
            data[attr] = getattr(elm, attr)
        if hasattr(elm, f"get_{attr}"):
            data[attr] = getattr(elm, f"get_{attr}")()
        elif raise_error:
            raise AttributeError(f"Attribute {attr} not found in {elm}")
    return data


@dataclass
class PlotPropertiesInfo(ArtistInfo):
    color: Optional[str] = None
    alpha: Optional[float] = None
    ls: Optional[str] = None
    lw: Optional[float] = None
    ds: Optional[str] = None
    marker: Optional[Union[str, int]] = None
    mfc: Optional[str] = None
    fc: Optional[str] = None
    mec: Optional[str] = None
    ec: Optional[str] = None
    ms: Optional[float] = None
    label: Optional[str] = None
    zorder: Optional[int] = None
    sizes: Optional[np.ndarray] = None
    hatch: Optional[str] = None

    @staticmethod
    def collect_data(elm, **kwargs):
        return collect_attributes(
            elm=elm,
            attributes=[
                "alpha",
                "ls",
                "lw",
                "ds",
                "marker",
                "color",
                "label",
                "mfc",
                "fc",
                "mec",
                "ec",
                "ms",
                "zorder",
                "sizes",
                "hatch",
            ],
            raise_error=False,
        )


@dataclass
class LineInfo(PlotPropertiesInfo):
    xdata: np.ndarray = None
    ydata: np.ndarray = None

    @classmethod
    def collect_data(cls, elm: lines.Line2D, **kwargs):
        xdata, ydata = elm.get_data()  # type: ignore
        return dict(
            xdata=xdata,
            ydata=ydata,
            **PlotPropertiesInfo.collect_data(elm, **kwargs),
        )

    def loads(self, /, **kwargs):
        ax: axes.Axes = kwargs["ax"]
        params = self.params()
        line = ax.add_line(lines.Line2D(**params))
        if self.transformation:
            self.transformation.load_to(line)

        return line


@dataclass
class ScatterInfo(PlotPropertiesInfo):
    xdata: np.ndarray = None
    ydata: np.ndarray = None

    @classmethod
    def collect_data(cls, elm: collections.PathCollection, **kwargs):
        xdata, ydata = elm.get_offsets().data.T  # type: ignore
        return dict(
            xdata=xdata,
            ydata=ydata,
            **PlotPropertiesInfo.collect_data(elm, **kwargs),
        )

    def loads(self, /, **kwargs):
        ax: axes.Axes = kwargs["ax"]
        params = self.params()
        x, y, s = params.pop("xdata"), params.pop("ydata"), params.pop("sizes")
        line = ax.scatter(x, y, s=s, **params)
        if self.transformation:
            self.transformation.load_to(line)

        return line


@dataclass
class RectangleInfo(PlotPropertiesInfo):
    xy: tuple = None
    width: float = None
    height: float = None
    angle: float = None
    rotation_point: float = None

    @classmethod
    def collect_data(cls, elm: patches.Rectangle, **kwargs):
        # break if xy='xy': (0.0, 0.0),
        return dict(
            xy=elm.get_xy(),
            width=elm.get_width(),
            height=elm.get_height(),
            angle=elm.angle,
            rotation_point=elm.rotation_point,
            **PlotPropertiesInfo.collect_data(elm, **kwargs),
        )

    def loads(self, /, **kwargs):
        ax: axes.Axes = kwargs["ax"]
        rect = patches.Rectangle(**self.params())

        rect = ax.add_patch(rect)

        if self.transformation:
            self.transformation.load_to(rect)
        return rect

    @classmethod
    def dumps_transformation(cls, elm, **kwargs):
        # Typically the transformation of the Rectangula is composed of
        # .get_patch_transform() and custom transform
        # No need to save get_patch_transform since it's applied automatically
        transformation = getattr(elm.get_transform(), "_b", None)
        if transformation:
            return TransformationInfo.dumps(transformation, ax=elm._axes)  # type: ignore
        return None


@dataclass
class BarInfo(ArtistInfo):
    def loads(self, /, **kwargs):
        for child in self.children:
            child.loads(**kwargs)


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
    def _dumps(elm: collections.LineCollection):
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
    grid: bool = False
    grid_alpha: Optional[float] = None
    aspect: Optional[str] = None
    spines: Optional[dict] = None
    xaxis_info: Optional[dict] = None
    yaxis_info: Optional[dict] = None

    _elm = axes.Axes

    @classmethod
    def collect_data(cls, elm: axes.Axes, **kwargs):
        # Get grid information
        grid_on = False
        grid_alpha = None
        try:
            # Check if grid is enabled
            grid_on = (
                elm.xaxis.get_gridlines()[0].get_visible()
                if elm.xaxis.get_gridlines()
                else False
            )
            if not grid_on and elm.yaxis.get_gridlines():
                grid_on = elm.yaxis.get_gridlines()[0].get_visible()
            if grid_on and elm.xaxis.get_gridlines():
                grid_alpha = elm.xaxis.get_gridlines()[0].get_alpha()
        except (IndexError, AttributeError):
            grid_on = False

        # Get aspect ratio
        aspect = elm.get_aspect()
        if aspect == "auto":
            aspect = None
        elif isinstance(aspect, (int, float)):
            aspect = str(aspect)

        # Get spine information
        spines = {}
        for spine_name, spine in elm.spines.items():
            spines[spine_name] = SpineInfo._dumps(spine).to_dict()

        # Get axis information
        xaxis_info = AxisInfo._dumps(elm.xaxis).to_dict()
        yaxis_info = AxisInfo._dumps(elm.yaxis).to_dict()

        return dict(
            xlim=elm.get_xlim(),
            ylim=elm.get_ylim(),
            rect=elm.get_position().bounds,
            xlabel=elm.get_xlabel(),
            ylabel=elm.get_ylabel(),
            title=elm.get_title(),
            grid=grid_on,
            grid_alpha=grid_alpha,
            aspect=aspect,
            spines=spines,
            xaxis_info=xaxis_info,
            yaxis_info=yaxis_info,
        )

    @classmethod
    def dumps(cls, ax: axes.Axes, dumps_func, objects_to_exclude: set = set()):
        objects_to_exclude.add(ax.patch)
        return super().dumps(ax, dumps_func, objects_to_exclude)

    def load_to(self, ax: axes.Axes, /):
        pass

    def loads(self, /, **kwargs):
        fig: figure.Figure = kwargs["fig"]
        ax = axes.Axes(fig=fig, rect=self.rect)

        ax.set_position(self.rect)

        if self.xlabel:
            ax.set_xlabel(self.xlabel)
        if self.ylabel:
            ax.set_ylabel(self.ylabel)
        if self.title:
            ax.set_title(self.title)

        # Restore grid
        if self.grid:
            ax.grid(True, alpha=self.grid_alpha)

        # Restore aspect ratio
        if self.aspect is not None:
            if self.aspect == "auto" or self.aspect == "equal":
                ax.set_aspect(self.aspect)
            else:
                try:
                    ax.set_aspect(float(self.aspect))
                except (ValueError, TypeError):
                    ax.set_aspect("auto")

        # Restore spine properties
        if self.spines:
            for spine_name, spine_data in self.spines.items():
                if spine_name in ax.spines:
                    spine_info = SpineInfo.from_dict(spine_data)
                    spine_info.apply_to_spine(ax.spines[spine_name])

        # Load children first (lines, etc.)
        for child in self.children:
            child.loads(ax=ax, **kwargs)

        # Then restore axis properties (ticks, scales, etc.) after the data is loaded
        if self.xaxis_info:
            xaxis_info = AxisInfo.from_dict(self.xaxis_info)
            xaxis_info.load_to(ax)

        if self.yaxis_info:
            yaxis_info = AxisInfo.from_dict(self.yaxis_info)
            yaxis_info.load_to(ax)

        # Restore basic axes properties
        ax.set_xlim(self.xlim)
        ax.set_ylim(self.ylim)

        fig.add_axes(ax)
        return ax


@dataclass
class LegendInfo(ArtistInfo):
    loc: int

    @staticmethod
    def _dumps(elm: legend.Legend):
        return LegendInfo(loc=elm._get_loc())  # pylint: disable=W0212 # type: ignore

    def load_to(self, ax: axes.Axes, /):
        ax.legend(loc=self.loc)

    def loads(self, /, **kwargs):
        obj = kwargs.get("ax", kwargs["fig"])
        obj.legend(loc=self.loc)


@dataclass
class FigureInfo(ArtistInfo):
    figsize: tuple = (6.4, 4.8)  # Default matplotlib figure size
    dpi: float = 100.0  # Default matplotlib DPI

    _elm = figure.Figure

    @classmethod
    def _dumps(cls, elm: figure.Figure):
        return FigureInfo(figsize=elm.get_size_inches(), dpi=elm.dpi)

    @classmethod
    def dumps(cls, elm: figure.Figure, dumps_func, objects_to_exclude: set = set()):
        objects_to_exclude.add(elm.patch)
        return super().dumps(elm, dumps_func, objects_to_exclude)

    def load(self, fig: figure.Figure, /, **kwargs):
        fig.set_size_inches(self.figsize)
        fig.set_dpi(self.dpi)
        for child in self.children:
            child.loads(fig=fig, **kwargs)

    def loads(self, /, **kwargs):
        fig = figure.Figure(figsize=self.figsize, dpi=self.dpi)
        self.load(fig, **kwargs)
        return fig


@dataclass
class SpineInfo(ArtistInfo):
    visible: bool = True
    color: Optional[str] = None
    linewidth: Optional[float] = None

    @staticmethod
    def _dumps(spine):
        """Create SpineInfo from matplotlib spine object"""
        return SpineInfo(
            visible=spine.get_visible(),
            color=spine.get_edgecolor(),
            linewidth=spine.get_linewidth(),
        )

    def apply_to_spine(self, spine):
        """Apply spine properties to matplotlib spine object"""
        spine.set_visible(self.visible)
        if self.color is not None:
            spine.set_color(self.color)
        if self.linewidth is not None:
            spine.set_linewidth(self.linewidth)


@dataclass
class AxisInfo(ArtistInfo):
    direction: Literal["x", "y"]
    ticks: Optional[list] = None
    ticklabels: Optional[list] = None
    scale: str = "linear"
    tick_params: Optional[dict] = None

    _elm = axis.Axis

    @classmethod
    def _dumps(cls, axis: axis.Axis):
        data = {}
        # Get direction from axis
        direction = "x" if hasattr(axis, "axis_name") and axis.axis_name == "x" else "y"
        if hasattr(axis.axes, "xaxis") and axis is axis.axes.xaxis:
            direction = "x"
        elif hasattr(axis.axes, "yaxis") and axis is axis.axes.yaxis:
            direction = "y"
        data["direction"] = direction

        # Get ticks and labels
        if not axis.isDefault_majloc or True:
            data["ticks"] = axis.get_ticklocs()
            data["ticklabels"] = (
                [t.get_text() for t in axis.get_ticklabels()]
                if axis.get_ticklabels()
                else None
            )
        if not axis.isDefault_minloc:
            data["minorticks"] = axis.get_ticklocs(minor=True)
            data["minorticklabels"] = [
                t.get_text() for t in axis.get_ticklabels(minor=True)
            ]

        # Get scale
        data["scale"] = (
            axis.axes.get_xscale() if direction == "x" else axis.axes.get_yscale()
        )

        # Get tick parameters
        data["tick_params"] = axis.get_tick_params()

        return cls(**data)

    def load_to(self, ax: axes.Axes, /):
        # Apply scale first
        if self.direction == "x":
            ax.set_xscale(self.scale)
        else:  # y
            ax.set_yscale(self.scale)

        # Apply ticks and labels
        if self.direction == "x":
            if self.ticks is not None:
                ax.set_xticks(self.ticks)
            if self.ticklabels is not None:
                ax.set_xticklabels(self.ticklabels)
        else:  # y
            if self.ticks is not None:
                ax.set_yticks(self.ticks)
            if self.ticklabels is not None:
                ax.set_yticklabels(self.ticklabels)

        # Apply tick parameters (including grid settings)
        if self.tick_params:
            # Handle grid separately if present
            tick_params = self.tick_params.copy()
            if tick_params.get("gridOn"):
                grid_alpha = tick_params.pop("grid_alpha", None)
                ax.grid(True, axis=self.direction, alpha=grid_alpha)
                tick_params.pop(
                    "gridOn", None
                )  # Remove gridOn as it's not a valid tick_params argument

            # Apply remaining tick parameters
            if tick_params:
                ax.tick_params(axis=self.direction, **tick_params)


@dataclass
class XAxisInfo(AxisInfo):
    direction = "x"


@dataclass
class YAxisInfo(AxisInfo):
    direction = "y"


@dataclass
class TextInfo(ArtistInfo):
    s: str
    xy: tuple
    rotation: float
    fontsize: float
    va: str
    ha: str
    color: str
    fontweight: str
    fontstyle: str
    # bbox: dict

    @classmethod
    def collect_data(cls, elm: mtext.Text, **kwargs):
        ax: axes.Axes = kwargs.get("ax", getattr(elm, "_axes"))
        if ax:
            if ax.title is elm:
                return None
        if elm.get_text() == "":
            return None
        return dict(
            s=elm.get_text(),
            xy=elm.get_unitless_position(),
            rotation=elm.get_rotation(),
            fontsize=elm.get_fontsize(),
            ha=elm.get_horizontalalignment(),
            va=elm.get_verticalalignment(),
            color=elm.get_color(),
            fontweight=elm.get_fontweight(),
            fontstyle=elm.get_fontstyle(),
        )

    def loads(self, /, **kwargs):
        ax: axes.Axes = kwargs.get("ax", kwargs["fig"])
        data = self.params()
        x, y = data.pop("xy")
        text = ax.text(x=x, y=y, **data)  # pylint: disable=W0212 # type: ignore

        if self.transformation:
            self.transformation.load_to(text, ax=ax)


@dataclass
class AnnotationInfo(TextInfo):
    xytext: tuple
    xycoords: str = "data"
    arrowprops: Optional[dict] = None

    @classmethod
    def collect_data(cls, elm: mtext.Text, **kwargs):
        data = super().collect_data(elm, **kwargs)
        data["xytext"] = (elm._x, elm._y)
        data["xy"] = elm.xy
        data["xycoords"] = elm.xycoords
        data["arrowprops"] = elm.arrowprops
        return data

    def loads(self, /, ax: axes.Axes, **kwargs):
        params = self.params()
        params["text"] = params.pop("s")
        ax.annotate(**params)
        # text = mtext.Annotation()
        # ax._add_text(text)  # pylint: disable=W0212 # type: ignore


@dataclass
class AxesImageInfo(ArtistInfo):
    data: np.ndarray
    aspect: float = 1.0
    extent: Optional[list] = None
    origin: str = "upper"
    cmap: Optional[str] = None

    @classmethod
    def _dumps(cls, elm: image.AxesImage):
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
    "ScatterInfo": ScatterInfo,
    "AxesInfo": AxesInfo,
    "LegendInfo": LegendInfo,
    "FigureInfo": FigureInfo,
    "LineCollectionInfo": LineCollectionInfo,
    "TransformationInfo": TransformationInfo,
    "SpineInfo": SpineInfo,
    "AxisInfo": AxisInfo,
    "XAxisInfo": XAxisInfo,
    "YAxisInfo": YAxisInfo,
    "AnnotationInfo": AnnotationInfo,
    "AxesImageInfo": AxesImageInfo,
    "TextInfo": TextInfo,
    "RectangleInfo": RectangleInfo,
    "BarInfo": BarInfo,
}
