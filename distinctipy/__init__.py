# -*- coding: utf-8 -*-
"""
distinctipy is a lightweight python package providing functions to generate
colours that are visually distinct from one another.

Example:
    >>> import distinctipy
    >>> distinctipy.get_colors(5)
    [(0, 1, 0), (1, 0, 1), (0, 0.5, 1), (1, 0.5, 0), (0.5, 0.75, 0.5)]
"""
# flake8: noqa
from importlib.metadata import version

name = "distinctipy"
__version__ = version(__name__)

# Expose these module names and their internals in the top-level API
__external__ = ["distinctipy"]

# Expose theses module names
__protected__ = ["colorsets", "colorblind"]

__autogen_notes__ = """
# Autogenerate this init file
pip install mkinit
mkinit -m distinctipy --relative --black
"""

# Everything after this point is autogenerate with mkinit
from . import colorblind, colorsets, distinctipy, examples
from .distinctipy import (
    BLACK,
    BLUE,
    CORNERS,
    CYAN,
    GREEN,
    INTERIOR,
    MAGENTA,
    MID_FACE,
    POINTS_OF_INTEREST,
    RED,
    WHITE,
    YELLOW,
    color_distance,
    color_swatch,
    distinct_color,
    get_colormap,
    get_colors,
    get_hex,
    get_random_color,
    get_rgb256,
    get_text_color,
    invert_colors,
)
from .examples import compare_clusters, compare_colors

__all__ = [
    "BLACK",
    "BLUE",
    "CORNERS",
    "CYAN",
    "GREEN",
    "INTERIOR",
    "MAGENTA",
    "MID_FACE",
    "POINTS_OF_INTEREST",
    "RED",
    "WHITE",
    "YELLOW",
    "color_distance",
    "color_swatch",
    "colorblind",
    "colorsets",
    "compare_clusters",
    "compare_colors",
    "distinct_color",
    "distinctipy",
    "examples",
    "get_colormap",
    "get_colors",
    "get_hex",
    "get_random_color",
    "get_rgb256",
    "get_text_color",
    "invert_colors",
    "name",
]
