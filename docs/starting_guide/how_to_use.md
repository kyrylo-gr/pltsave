# How to use pltsave

Make sure you have [installed the package](install.md) before.

## Usage

Save a figure:

```python
import pltsave

figure_info = pltsave.dumps(fig).to_json()
```

Load the figure

```python
fig = pltsave.loads(figure_info)
```
