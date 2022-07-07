"""
Provides access to a large list of 200 colors for "normal" and "deuteranomaly"
vision.
"""
from . import distinctipy
from ._colorsets_data import colors


def list_colorsets():
    """
    Get a list of the names of built-in distinctipy colours.

    :return: A tuple of keys present in the dictionary distinctipy.colorsets.colors
    """
    return tuple(["colorblind"] + list(colors.keys()))


def __process_name(name):
    """
    Map the name colorblind to deuteranomaly (most common type of common blindness)
    """
    if name == "colorblind":
        return "deuteranomaly"
    else:
        return name


def get_colormap(name="normal"):
    """
    Get a matplotlib colormap of built-in colours generated with distinctipy.

    :param name: The name of a colour set present in
        distinctipy.colorsets.list_colorsets()

    :return: A matplotlib ListedColorMap for the colors in
        distinctipy.colorsets.colors[name].
    """
    name = __process_name(name)
    assert name in list_colorsets(), "name should exist in " + str(list_colorsets())

    return distinctipy.get_colormap(colors[name], name="distinctipy_" + name)


def get_colors(name="normal"):
    """
    Return a list of built-in colours generated with distinctipy.

    :param name: The name of a colour set present in
        distinctipy.colorsets.list_colorsets()

    :return: A list of (r,g,b) colour tuples, where r, g and b are floats between 0
        and 1.
    """
    name = __process_name(name)
    assert name in list_colorsets(), "name should exist in " + str(list_colorsets())

    return colors[name]


def set_palette(name="normal"):
    """
    Set the default colour palette used by matplotlib to distinctipy colours.

    :param name: The name of a colour set present in
        distinctipy.colorsets.list_colorsets()
    """
    import matplotlib as mpl

    name = __process_name(name)
    assert name in list_colorsets(), "name should exist in " + str(list_colorsets())

    mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=colors[name])
    mpl.rcParams["patch.facecolor"] = colors[name][0]
