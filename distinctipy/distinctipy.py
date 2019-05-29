import random
import math
import numpy as np

import matplotlib.colors
import matplotlib.patches as patches
import matplotlib.pyplot as plt

from distinctipy import colorblind

WHITE = (1.0, 1.0, 1.0)
BLACK = (0.0, 0.0, 0.0)


def get_random_color(pastel_factor=0):
    """
    Generate a random rgb colour.

    :param pastel_factor: float between 0 and 1. If pastel_factor>0 paler colours will be generated.

    :return: color: a (r,g,b) tuple. r, g and b are values between 0 and 1.
    """

    color = [(random.random() + pastel_factor) / (1.0 + pastel_factor) for _ in range(3)]

    return tuple(color)


def color_distance(c1, c2):
    """
    Metric to define the visual distinction between two (r,g,b) colours.
    Inspired by: https://www.compuphase.com/cmetric.htm

    :param c1: (r,g,b) colour tuples. r,g and b are values between 0 and 1.
    :param c2: (r,g,b) colour tuples. r,g and b are values between 0 and 1.
    :param colorblind_type: generate colours that are distinct with given type of colourblindness

    :return: distance: float representing visual distinction between c1 and c2. Larger values = more distinct.
    """

    r1, g1, b1 = c1
    r2, g2, b2 = c2

    mean_r = (r1 + r2) / 2
    delta_r = (r1 - r2) ** 2
    delta_g = (g1 - g2) ** 2
    delta_b = (b1 - b2) ** 2

    distance = (2 + mean_r) * delta_r + 4 * delta_g + (3 - mean_r) * delta_b

    return distance


def distinct_color(exclude_colors, pastel_factor=0, n_attempts=1000, colorblind_type=None):
    """
    Generate a colour as distinct as possible from the colours defined in exclude_colors.
    Inspired by: https://gist.github.com/adewes/5884820

    :param exclude_colors: a list of (r,g,b) tuples. r,g,b are values between 0 and 1.
    :param pastel_factor: float between 0 and 1. If pastel_factor>0 paler colours will be generated.
    :param n_attempts: number of random colours to generate to find most distinct colour

    :param colorblind_type: Type of colourblindness to simulate, can be:
        'Normal': Normal vision
        'Protanopia': Red-green colorblindness (1% males)
        'Protanomaly': Red-green colorblindness (1% males, 0.01% females)
        'Deuteranopia': Red-green colorblindness (1% males)
        'Deuteranomaly': Red-green colorblindness (most common type: 6% males, 0.4% females)
        'Tritanopia': Blue-yellow colourblindness (<1% males and females)
        'Tritanomaly' Blue-yellow colourblindness (0.01% males and females)
        'Achromatopsia': Total colourblindness
        'Achromatomaly': Total colourblindness

    :return: (r,g,b) color tuple of the generated colour with the largest minimum color_distance to the colours in exclude_colors.
    """

    if colorblind_type is not None:
        exclude_colors = [colorblind.colorblind_filter(color, colorblind_type) for color in exclude_colors]

    max_distance = None
    best_color = None

    for _ in range(n_attempts):
        color = get_random_color(pastel_factor=pastel_factor)

        if not exclude_colors:
            return color

        else:
            if colorblind_type is not None:
                compare_color = colorblind.colorblind_filter(color, colorblind_type)
            else:
                compare_color = color

            distance_to_nearest = min([color_distance(compare_color, c) for c in exclude_colors])

            if (not max_distance) or (distance_to_nearest > max_distance):
                max_distance = distance_to_nearest
                best_color = color

    return tuple(best_color)


def get_text_color(background_color, threshold=0.6):
    """
    Choose whether black or white text will work better on top of background_color.
    Inspired by: https://stackoverflow.com/a/3943023

    :param background_color: The colour the text will be displayed on
    :param threshold: float between 0 and 1. With threshold close to 1 white text will be chosen more often.

    :return: (0,0,0) if black text should be used or (1,1,1) if white text should be used.
    """

    r, g, b = background_color[0], background_color[1], background_color[2]

    if (r * 0.299 + g * 0.587 + b * 0.114) > threshold:
        return BLACK
    else:
        return WHITE

    return text_color


def get_colors(n_colors, exclude_colors=None, return_excluded=False,
               pastel_factor=0, n_attempts=1000, colorblind_type=None):
    """
    Generate a list of n visually distinct colours.

    :param n_colors: How many colours to generate

    :param exclude_colors: A pre-existing list of (r,g,b) colours that new colours should be distinct from.
    If exclude_colours=None then exclude_colours will be set to avoid white and black (exclude_colours=[(0,0,0), (1,1,1)]).
    (r,g,b) values should be floats between 0 and 1.

    :param return_excluded: If return_excluded=True then exclude_colors will be included in the returned color list.
    Otherwise only the newly generated colors are returned (default).

    :param pastel_factor: float between 0 and 1. If pastel_factor>0 paler colours will be generated.

    :param n_attempts: number of random colours to generated to find most distinct colour.

    :param colorblind_type: generate colours that are distinct with given type of colourblindness. Can be:
        'Normal': Normal vision
        'Protanopia': Red-green colorblindness (1% males)
        'Protanomaly': Red-green colorblindness (1% males, 0.01% females)
        'Deuteranopia': Red-green colorblindness (1% males)
        'Deuteranomaly': Red-green colorblindness (most common type: 6% males, 0.4% females)
        'Tritanopia': Blue-yellow colourblindness (<1% males and females)
        'Tritanomaly' Blue-yellow colourblindness (0.01% males and females)
        'Achromatopsia': Total colourblindness
        'Achromatomaly': Total colourblindness

    :return: colors - A list of (r,g,b) colors that are visually distinct to each other and to the colours in exclude_colors.
    (r,g,b) values are floats between 0 and 1.
    """

    if exclude_colors is None:
        exclude_colors = [WHITE, BLACK]

    colors = exclude_colors.copy()

    for i in range(n_colors):
        colors.append(distinct_color(colors, pastel_factor=pastel_factor,
                                     n_attempts=n_attempts, colorblind_type=colorblind_type))

    if return_excluded:
        return colors
    else:
        return colors[len(exclude_colors):]


def invert_colors(colors, exclude_black=False, exclude_white=False, pastel_factor=0, n_attempts=1000):
    """
    Generates inverted colours for each colour in the given colour list, i.e. colours that are as distinct as possible
     from each colour in the list.

    :param colors: A list of (r,g,b) colour tuples. (r,g,b) values should be floats between 0 and 1.
    :param exclude_black: If True, don't generate black as an inverted colour.
    :param exclude_white: If True, don't generate white as an inverted colour.
    :param pastel_factor:  float between 0 and 1. If pastel_factor>0 paler colours will be generated.
    :param n_attempts: number of random colours to generated to find most distinct colour.

    :return: inverted_colors - A list of (r,g,b) colors that are visually distinct to each other and to the colours in exclude_colors.
    (r,g,b) values are floats between 0 and 1.
    """
    inverted_colors = []

    for color in colors:
        color = [color]

        if exclude_black:
            color.append(BLACK)

        if exclude_white:
            color.append(WHITE)

        inverted_colors.append(distinct_color(color, pastel_factor=pastel_factor, n_attempts=n_attempts))

    return inverted_colors


def get_colormap(colors):
    """
    Converts a list of colors into a matplotlib colormap.

    :param colors: a list of (r,g,b) color tuples. (r,g,b) values should be floats between 0 and 1.

    :return: cmap: a matplotlib colormap.
    """
    cmap = matplotlib.colors.ListedColormap(colors)

    return cmap


def color_swatch(colors, edgecolors=None, show_text=False, text_threshold=0.6,
                 ax=None, title=None, one_row=None,):
    """
    Display the colours defined in a list of colors.

    :param colors: List of (r,g,b) colour tuples to display. (r,g,b) should be floats between 0 and 1.
    :param edgecolors: If None displayed colours have no outline. Otherwise a list of (r,g,b) colours used as an outline.
    :param show_text: If True writes the background colour's hex on top of it in black or white, as appropriate.
    :param text_threshold: float between 0 and 1. With threshold close to 1 white text will be chosen more often.
    :param ax: Matplotlib axis to plot to. If ax is None plt.show() is run in function call.
    :param title: Add a title to the colour swatch.
    :param one_row: If True display colours on one row, if False as a grid. If one_row=None a grid is used when there
    are more than 8 colours.
    :return:
    """
    if one_row is None:
        if len(colors) > 8:
            one_row = False
        else:
            one_row = True

    if one_row:
        n_grid = len(colors)
    else:
        n_grid = math.ceil(np.sqrt(len(colors)))

    width = 1
    height = 1

    x = 0
    y = 0

    max_x = 0
    max_y = 0

    if ax is None:
        show = True
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, aspect='equal')
    else:
        show = False

    for idx, color in enumerate(colors):
        if edgecolors is None:
            ax.add_patch(patches.Rectangle((x, y), width, height, color=color))
        else:
            ax.add_patch(patches.Rectangle((x, y), width, height, facecolor=color,
                                           edgecolor=edgecolors[idx], linewidth=5))

        if show_text:
            ax.text(x+(width/2), y+(height/2), matplotlib.colors.rgb2hex(color),
                    fontsize=80/np.sqrt(len(colors)), ha='center',
                    color=get_text_color(color, threshold=text_threshold))

        if (idx + 1) % n_grid == 0:
            if edgecolors is None:
                y += height
                x = 0
            else:
                y += height + (height/10)
                x = 0
        else:
            if edgecolors is None:
                x += width
            else:
                x += width + (width/10)

        if x > max_x:
            max_x = x

        if y > max_y:
            max_y = y

    ax.set_ylim([-height/10, max_y+1.1*height])
    ax.set_xlim([-width/10, max_x+1.1*width])
    ax.invert_yaxis()
    ax.axis('off')

    if title is not None:
        ax.set_title(title)

    if show:
        plt.show()


def get_hex(color):
    """
    Returns hex of given color
    :param color: (r,g,b) color tuple. r,g,b are floats between 0 and 1.
    :return: hex str of color
    """
    return matplotlib.colors.rgb2hex(color)


def get_rgb256(color):
    """
    Converts 0.0-1.0 rgb colour into 0-255 integer rgb colour
    :param color: (r,g,b) tuple with r,g,b floats between 0.0 and 1.0
    :return: (r,g,b) ints between 0 and 255
    """
    return round(color[0]*255), round(color[1]*255), round(color[2]*255)
