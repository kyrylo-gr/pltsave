import matplotlib as mpl

DEFAULT_COLORS = dict(enumerate(mpl.rcParams["axes.prop_cycle"].by_key()["color"]))

DEFAULT_COLORS_REVERSE = {v: k for k, v in DEFAULT_COLORS.items()}

DEFAULT_VALUES = {
    "linewidth": mpl.rcParams["lines.linewidth"],
    "linestyle": "-",  # mpl.rcParams["lines.linestyle"]
    "drawstyle": "default",
    "marker": "None",
    "alpha": None,
}
