KEY_ALIASES_MAP = {
    "xlim": "xl",
    "ylim": "yl",
    "xdata": "xd",
    "ydata": "yd",
    "xlabel": "xb",
    "ylabel": "yb",
    "children": "x",
    "color": "c",
    "marker": "m",
    "markersize": "ms",
    "markerfacecolor": "mfc",
    "markeredgewidth": "mew",
    "markeredgecolor": "mec",
    "linestyle": "ls",
    "linewidth": "lw",
    "drawstyle": "ds",
    "label": "l",
    "zorder": "z",
    "__name__": "n",
}

KEY_ALIASES_INVERSE = {v: k for k, v in KEY_ALIASES_MAP.items()}

TEXT_FORBIDDEN_SYMBOLS = set(",[]{}()")

SHORT_NAMES_OF_CLASSES_INVERSE = {
    "Line": "LineInfo",
    "Scatter": "ScatterInfo",
    "Axes": "AxesInfo",
    "Legend": "LegendInfo",
    "Figure": "FigureInfo",
    "LineCollection": "LineCollectionInfo",
    "Transformation": "TransformationInfo",
    "Spine": "SpineInfo",
    "Axis": "AxisInfo",
    "XAxis": "XAxisInfo",
    "YAxis": "YAxisInfo",
    "Annotation": "AnnotationInfo",
    "AxesImage": "AxesImageInfo",
    "Text": "TextInfo",
    "Rectangle": "RectangleInfo",
    "Bar": "BarInfo",
}

SHORT_NAMES_OF_CLASSES = {v: k for k, v in SHORT_NAMES_OF_CLASSES_INVERSE.items()}
