import json
import typing as _t

import matplotlib.pyplot as plt
from matplotlib import collections, image, legend, lines, text
from matplotlib.artist import Artist
from matplotlib.figure import Figure

from . import json_coders
from .aliases import SHORT_NAMES_OF_CLASSES_INVERSE
from .compress.routines import decode_dict
from .stuctures import (  # XAxisInfo,; YAxisInfo,
    NAMES_OF_CLASSES,
    AnnotationInfo,
    ArtistInfo,
    AxesImageInfo,
    AxesInfo,
    FigureInfo,
    LegendInfo,
    LineCollectionInfo,
    LineInfo,
    TransformationInfo,
)


@_t.overload
def dumps(elm: "Figure") -> FigureInfo: ...  # noqa: E704


@_t.overload
def dumps(elm: "plt.Axes") -> AxesInfo: ...  # noqa: E704


@_t.overload
def dumps(elm: "lines.Line2D") -> LineInfo: ...  # noqa: E704


def dumps(elm):
    if isinstance(elm, plt.Axes):
        info = AxesInfo.dumps(elm)
    elif isinstance(elm, Figure):
        info = FigureInfo.dumps(elm)
    elif isinstance(elm, lines.Line2D):
        info = LineInfo.dumps(elm)
    elif isinstance(elm, legend.Legend):
        info = LegendInfo.dumps(elm)
    elif isinstance(elm, collections.LineCollection):
        info = LineCollectionInfo.dumps(elm)
    # elif isinstance(elm, mpl.axis.XAxis):
    #     info = XAxisInfo.dumps(elm)
    # elif isinstance(elm, mpl.axis.YAxis):
    # info = YAxisInfo.dumps(elm)
    elif isinstance(elm, text.Annotation):
        info = AnnotationInfo.dumps(elm)
    elif isinstance(elm, image.AxesImage):
        info = AxesImageInfo.dumps(elm)
    else:
        return None

    if info is None:
        return None

    for child in elm.get_children():
        child_info = dumps(child)  # type: ignore
        if child_info:
            info.children.append(child_info)

    transformation = elm.get_transform()

    if transformation:
        info.transformation = TransformationInfo.dumps_from_obj(elm)  # type: ignore

    return info


def load_axes(ax: plt.Axes, info: AxesInfo):
    for child in info.children:
        child.load_to(ax)

    return info


def load_fig(fig, info: FigureInfo):
    for child in info.children:
        # getattr(obj, child._func)(child._elm(**child.dict()))
        if child.__class__.__name__ == "AxesInfo":
            ax = plt.Axes(fig, **child.params())
            load_axes(ax, child)  # type: ignore
            fig.add_axes(ax)
        if child.__class__.__name__ == "LegendInfo":
            fig.legend(loc=child.loc)  # type: ignore

    return info


def load(obj, info):
    if isinstance(info, str):
        info = info_from_str(info)

    if isinstance(info, dict):
        info = FigureInfo.from_dict(info)

    info.load_to(obj)

    # if isinstance(info, FigureInfo): # info.__class__.__name__ == "FigureInfo"
    #     return load_fig(obj, info)
    # if isinstance(info, AxesInfo): # info.__class__.__name__ == "AxesInfo"
    #     return load_axes(obj, info)
    return info


def loads(code: _t.Union[str, dict, ArtistInfo]) -> "Artist":
    if isinstance(code, str):
        info = info_from_str(code)
    elif isinstance(code, dict):
        class_itself = get_class_by_short_name(code["__name__"])
        info = class_itself.from_dict(code)
    else:
        info = code

    return info.loads()


def loads_fig(code: _t.Union[str, dict, ArtistInfo]) -> "Figure":
    return loads(code)  # type: ignore


def loads_ax(code: _t.Union[str, dict, ArtistInfo]) -> "plt.Axes":
    return loads(code)  # type: ignore


# _T = _t.TypeVar("_T", bound=Artist)


# class LoadedResult(_t.Generic[_T], _t.NamedTuple):
#     obj: _T
#     info: ArtistInfo


def info_from_str(code: str):
    if code.startswith("{"):
        data = json.loads(code, cls=json_coders.NumbersDecoder)
    else:
        data = decode_dict(code)

    class_itself = get_class_by_short_name(data["__name__"])
    return class_itself.from_dict(data)


def get_class_by_short_name(name: str) -> _t.Type[ArtistInfo]:
    class_name = SHORT_NAMES_OF_CLASSES_INVERSE[name]
    return NAMES_OF_CLASSES[class_name]
