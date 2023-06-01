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

figure_info = pltsave.dumps(fig).to_json()
```

Load the figure

```python
fig = pltsave.loads(fig2)
```
