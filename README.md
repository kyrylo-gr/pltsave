# Pltsave. Super easy way to save and open matplotlib plots.

<h1 align="center">
<img src="docs/images/pltsave-small.png" height="200">
</h1>
<br/>

<div align="center">

<img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python 3.8+">
<a href="https://github.com/kyrylo-gr/pltsave/blob/main/LICENCE">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</a>
<a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
</a>
<a href="https://www.codefactor.io/repository/github/kyrylo-gr/pltsave/overview/main">
    <img src="https://www.codefactor.io/repository/github/kyrylo-gr/pltsave/badge/main" alt="CodeFactor">
</a>
<a href="https://pypistats.org/packages/pltsave">
    <img src="https://img.shields.io/pypi/dm/pltsave" alt="Download Stats">
</a>
<a href="https://kyrylo-gr.github.io/pltsave/">
    <img src="https://img.shields.io/badge/docs-blue" alt="Documentation">
</a>
</div>

## Install

`pip install pltsave`

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

## That's it.

It's as easy as it looks. See [the documentation](https://kyrylo-gr.github.io/pltsave/) for more information and examples.
