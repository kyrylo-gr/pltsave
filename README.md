## Install

`pip install pltsave`

## Installation in dev mode

`pip install -e .[dev]`

or

`python setup.py develop`

## Usage

Save a figure:

```python
import pltsave

figure_info = pltsave.dumps(fig)
```

Load the figure

```python
fig2 = plt.figure()
pltsave.load_fig(fig2, figure_info)
```
