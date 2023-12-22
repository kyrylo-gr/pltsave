from typing import overload
import matplotlib as mpl
import matplotlib.pyplot as plt

from .stuctures import (
    LineInfo,
    AxesInfo,
    LegendInfo,
    FigureInfo,
    LineCollectionInfo,
    TransformationInfo,
    XAxisInfo,
    YAxisInfo,
    AnnotationInfo,
)


@overload
def dumps(elm: "plt.Figure") -> FigureInfo:
    ...


@overload
def dumps(elm: "plt.Axes") -> AxesInfo:
    ...


@overload
def dumps(elm: "mpl.lines.Line2D") -> LineInfo:
    ...


def dumps(elm):
    if isinstance(elm, plt.Axes):
        info = AxesInfo.dumps(elm)
    elif isinstance(elm, plt.Figure):
        info = FigureInfo.dumps(elm)
    elif isinstance(elm, mpl.lines.Line2D):
        info = LineInfo.dumps(elm)
    elif isinstance(elm, mpl.legend.Legend):
        info = LegendInfo.dumps(elm)
    elif isinstance(elm, mpl.collections.LineCollection):
        info = LineCollectionInfo.dumps(elm)
    elif isinstance(elm, mpl.axis.XAxis):
        info = XAxisInfo.dumps(elm)
    elif isinstance(elm, mpl.axis.YAxis):
        info = YAxisInfo.dumps(elm)
    elif isinstance(elm, mpl.text.Annotation):
        info = AnnotationInfo.dumps(elm)
    else:
        return None

    if info is None:
        return None

    for child in elm.get_children():
        child_info = dumps(child)
        if child_info:
            info.children.append(child_info)

    transformation = elm.get_transform()

    if transformation:
        info.transformation = TransformationInfo.dumps_from_obj(elm)

    return info


def load_axes(ax: plt.Axes, info: AxesInfo):
    for child in info.children:
        child.load_to(ax)


def load_fig(fig, info: FigureInfo):
    for child in info.children:
        # getattr(obj, child._func)(child._elm(**child.dict()))
        if child.__class__.__name__ == "AxesInfo":
            ax = plt.Axes(fig, **child.params())
            load_axes(ax, child)
            fig.add_axes(ax)
        if child.__class__.__name__ == "LegendInfo":
            fig.legend(loc=child.loc)


def load(obj, info) -> None:
    if isinstance(info, str):
        info = FigureInfo.from_json(info)
    if isinstance(info, dict):
        info = FigureInfo.from_dict(info)

    if info.__class__.__name__ == "FigureInfo":
        return load_fig(obj, info)
    if info.__class__.__name__ == "AxesInfo":
        return load_axes(obj, info)


def loads(info) -> "plt.Figure":
    fig = plt.figure()
    load(fig, info)
    return fig
