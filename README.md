![distinctipy logo](https://raw.githubusercontent.com/alan-turing-institute/distinctipy/master/distinctipy_logo.png)

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

```python
pip3 install distinctipy
```

Alternatively clone the repo and then in its parent directory run:
```bash
pip3 install -r requirements.txt
pip3 install .
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
* Attempt to generate colours as distinct as possible for someone with colourblindness `distinctipy.get_colors(N, existing_colors)`

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

More detailed usage and example output can be found in the notebook **[examples.ipynb](https://github.com/alan-turing-institute/distinctipy/blob/master/examples.ipynb)** and **[examples gallery](https://github.com/alan-turing-institute/distinctipy/tree/master/examples)**.

## References

*distinctipy* was heavily influenced and inspired by several web sources and
stack overflow answers. In particular:
* **Random generation of distinct colours:** [Andrew Dewes on GitHub](https://gist.github.com/adewes/5884820)
* **Colour distance metric:** [Thiadmer Riemersma at CompuPhase](https://www.compuphase.com/cmetric.htm)
* **Best text colour for background:** [Mark Ransom on Stack Overflow](https://stackoverflow.com/a/3943023)
* **Colourblindness Filters:** [Matthew Wickline and the Human-Computer Interaction Resource Network](http://web.archive.org/web/20090318054431/http://www.nofunc.com/Color_Blindness_Library) (web archive)

Thanks!
