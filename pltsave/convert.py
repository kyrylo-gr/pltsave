import matplotlib as mpl
import matplotlib.pyplot as plt

from .stuctures import LineInfo, AxesInfo, LegendInfo, FigureInfo


def dumps(elm):
    if isinstance(elm, plt.Axes):
        info = AxesInfo.from_mpl(elm)
    elif isinstance(elm, plt.Figure):
        info = FigureInfo.from_mpl(elm)
    elif isinstance(elm, mpl.lines.Line2D):
        info = LineInfo.from_mpl(elm)
    elif isinstance(elm, mpl.legend.Legend):
        info = LegendInfo.from_mpl(elm)
    else:
        return None

    for child in elm.get_children():
        child_info = dumps(child)
        if child_info:
            info.children.append(child_info)

    return info


def load_axes(ax: plt.Axes, info: AxesInfo):
    for child in info.children:
        if isinstance(child, LineInfo):
            getattr(ax, child._func)(child._elm(  # pylint: disable=W0212
                **child.params()))
        elif isinstance(child, LegendInfo):
            ax.legend(loc=child.loc)


def load_fig(fig, info: FigureInfo):
    for child in info.children:
        # getattr(obj, child._func)(child._elm(**child.dict()))
        if isinstance(child, AxesInfo):
            ax = plt.Axes(fig, **child.params())
            load_axes(ax, child)
            fig.add_axes(ax)
        if isinstance(child, LegendInfo):
            fig.legend(loc=child.loc)


def load(obj, info):
    if isinstance(info, FigureInfo):
        return load_fig(obj, info)
    if isinstance(info, AxesInfo):
        return load_axes(obj, info)
