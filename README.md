![distinctipy logo](https://raw.githubusercontent.com/alan-turing-institute/distinctipy/main/distinctipy_logo.png)


![tests](https://github.com/alan-turing-institute/distinctipy/workflows/Tests/badge.svg)
![build](https://github.com/alan-turing-institute/distinctipy/workflows/Build/badge.svg)
[![codecov](https://codecov.io/gh/alan-turing-institute/distinctipy/branch/main/graph/badge.svg)](https://codecov.io/gh/alan-turing-institute/distinctipy)
[![DOI](https://zenodo.org/badge/188444660.svg)](https://zenodo.org/badge/latestdoi/188444660)
[![Documentation Status](https://readthedocs.org/projects/distinctipy/badge/?version=latest)](https://distinctipy.readthedocs.io/en/latest/?badge=latest)

*distinctipy* is a lightweight python package providing functions to generate
colours that are visually distinct from one another.

Commonly available qualitative colormaps provided by the likes of matplotlib
generally have no more than 20 colours, but for some applications it is useful
to have many more colours that are clearly different from one another.
*distinctipy* can generate lists of colours of any length, with each new colour
added to the list being as visually distinct from the pre-existing colours in
 the list as possible.

## Installation

*distinctipy* is designed for Python 3 and can be installed with pip by running:

```shell
pip install distinctipy
```

Alternatively clone the repo and install it locally:

```shell
git clone https://github.com/alan-turing-institute/distinctipy.git
cd distinctipy
pip install .
```

### Optional Dependencies

Starting in version 1.2.1 `distinctipy` no longer bundles `matplotlib`, `pandas` or dev dependencies in the default installation. If you wish to view
colours (e.g. with `distinctipy.color_swatch`) or examples you will need `matplotlib` and `pandas` installed. To do this, either install `distinctipy`
with the optional flag:
```bash
pip install distinctipy[optional]
```

Or install them separately:
```bash
pip install matplotlib pandas
```

For developers, to install the stack needed to run tests, generate docs etc. use the `[all]` flag:
```bash
pip install distinctipy[all]
```

## Usage and Examples

*distinctipy* can:
* Generate N visually distinct colours: `distinctipy.get_colors(N)`
* Generate colours that are distinct from an existing list of colours: `distinctipy.get_colors(N, existing_colors)`
* Generate pastel colours: `distinctipy.get_colors(N, pastel_factor=0.7)`
* Select black or white as the best font colour for any background colour: `distinctipy.get_text_color(background_color)`
* Convert lists of colours into matplotlib colormaps: `distinctipy.get_colormap(colors)`
* Invert colours: `distinctipy.invert_colors(colors)`
* Nicely display generated colours: `distinctipy.color_swatch(colors)`
* Compare distinctipy colours to other common colormaps: `examples.compare_clusters()` and `examples.compare_colors()`
* Simulate how colours look for someone with colourblindness: `colorblind.simulate_colors(colors, colorblind_type='Deuteranomaly')`
* Attempt to generate colours as distinct as possible for someone with colourblindness `distinctipy.get_colors(N, existing_colors, colorblind_type="Deuteranomaly")`

For example, to create and then display N = 36 visually distinct colours:

```python
from distinctipy import distinctipy

# number of colours to generate
N = 36

# generate N visually distinct colours
colors = distinctipy.get_colors(N)

# display the colours
distinctipy.color_swatch(colors)
```

More detailed usage and example output can be found in the notebook **[examples.ipynb](https://github.com/alan-turing-institute/distinctipy/blob/main/examples.ipynb)** and **[examples gallery](https://github.com/alan-turing-institute/distinctipy/tree/main/examples)**.

## References

*distinctipy* was heavily influenced and inspired by several web sources and
stack overflow answers. In particular:
* **Random generation of distinct colours:** [Andrew Dewes on GitHub](https://gist.github.com/adewes/5884820)
* **Colour distance metric:** [Thiadmer Riemersma at CompuPhase](https://www.compuphase.com/cmetric.htm)
* **Best text colour for background:** [Mark Ransom on Stack Overflow](https://stackoverflow.com/a/3943023)
* **Colourblindness Filters:** [Matthew Wickline and the Human-Computer Interaction Resource Network](http://web.archive.org/web/20090318054431/http://www.nofunc.com/Color_Blindness_Library) (web archive)

## Citing distinctipy

If you would like to cite distinctipy, please refer to the upload of the package on Zenodo: https://doi.org/10.5281/zenodo.3985191
