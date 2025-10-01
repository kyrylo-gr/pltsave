import json
import typing as _t

import matplotlib.pyplot as plt
from matplotlib import collections, container, image, legend, lines, patches, text
from matplotlib.artist import Artist
from matplotlib.figure import Figure

from . import json_coders
from .aliases import SHORT_NAMES_OF_CLASSES_INVERSE
from .compress.routines import decode_dict
from . import stuctures
# from .stuctures import (  # XAxisInfo,; YAxisInfo,
#     NAMES_OF_CLASSES,
#     AnnotationInfo,
#     ArtistInfo,
#     AxesImageInfo,
#     AxesInfo,
#     FigureInfo,
#     LegendInfo,
#     LineCollectionInfo,
#     LineInfo,
#     ScatterInfo,
#     TextInfo,
#     TransformationInfo,
# )


@_t.overload
def dumps(elm: "Figure") -> stuctures.FigureInfo: ...  # noqa: E704


@_t.overload
def dumps(elm: "plt.Axes") -> stuctures.AxesInfo: ...  # noqa: E704


@_t.overload
def dumps(elm: "lines.Line2D") -> stuctures.LineInfo: ...  # noqa: E704


def dumps(elm):
    if isinstance(elm, plt.Axes):
        info = stuctures.AxesInfo.dumps(elm, dumps)
    elif isinstance(elm, Figure):
        info = stuctures.FigureInfo.dumps(elm, dumps)
    elif isinstance(elm, lines.Line2D):
        info = stuctures.LineInfo.dumps(elm, dumps)
    elif isinstance(elm, collections.PathCollection):
        info = stuctures.ScatterInfo.dumps(elm, dumps)
    elif isinstance(elm, legend.Legend):
        info = stuctures.LegendInfo.dumps(elm, dumps)
    elif isinstance(elm, collections.LineCollection):
        info = stuctures.LineCollectionInfo.dumps(elm, dumps)
    elif isinstance(elm, text.Annotation):
        info = stuctures.AnnotationInfo.dumps(elm, dumps)
    elif isinstance(elm, text.Text):
        info = stuctures.TextInfo.dumps(elm, dumps)
    elif isinstance(elm, container.BarContainer):
        info = stuctures.BarInfo.dumps(elm, dumps)
    elif isinstance(elm, patches.Rectangle):
        info = stuctures.RectangleInfo.dumps(elm, dumps)

    # elif isinstance(elm, mpl.axis.XAxis):
    #     info = XAxisInfo.dumps(elm)
    # elif isinstance(elm, mpl.axis.YAxis):
    # info = YAxisInfo.dumps(elm)

    elif isinstance(elm, image.AxesImage):
        info = stuctures.AxesImageInfo.dumps(elm, dumps)
    else:
        return None

    if info is None:
        return None

    return info


def load_axes(ax: plt.Axes, info: stuctures.AxesInfo):
    for child in info.children:
        child.load_to(ax)

    return info


def load_fig(fig, info: stuctures.FigureInfo):
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
        info = stuctures.FigureInfo.from_dict(info)

    info.load_to(obj)

    # if isinstance(info, FigureInfo): # info.__class__.__name__ == "FigureInfo"
    #     return load_fig(obj, info)
    # if isinstance(info, AxesInfo): # info.__class__.__name__ == "AxesInfo"
    #     return load_axes(obj, info)
    return info


def loads(code: _t.Union[str, dict, stuctures.ArtistInfo]) -> "Artist":
    if isinstance(code, str):
        info = info_from_str(code)
    elif isinstance(code, dict):
        class_itself = get_class_by_short_name(code["__name__"])
        info = class_itself.from_dict(code)
    else:
        info = code

    return info.loads()


def loads_fig(code: _t.Union[str, dict, stuctures.ArtistInfo]) -> "Figure":
    return loads(code)  # type: ignore


def loads_ax(code: _t.Union[str, dict, stuctures.ArtistInfo]) -> "plt.Axes":
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


def get_class_by_short_name(name: str) -> _t.Type[stuctures.ArtistInfo]:
    class_name = SHORT_NAMES_OF_CLASSES_INVERSE[name]
    return stuctures.NAMES_OF_CLASSES[class_name]
