"""
Adapted from "The Color Blind Simulation function" by Matthew Wickline
and the Human - Computer Interaction Resource Network (http://hcirn.com/), 2000 - 2001.
"""
import numpy as np

rBlind = {
    "protan": {"cpu": 0.735, "cpv": 0.265, "am": 1.273463, "ayi": -0.073894},
    "deutan": {"cpu": 1.14, "cpv": -0.14, "am": 0.968437, "ayi": 0.003331},
    "tritan": {"cpu": 0.171, "cpv": -0.003, "am": 0.062921, "ayi": 0.292119},
}


def rgb2xyz(rgb):
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]

    x = 0.430574 * r + 0.341550 * g + 0.178325 * b
    y = 0.222015 * r + 0.706655 * g + 0.071330 * b
    z = 0.020183 * r + 0.129553 * g + 0.939180 * b

    return x, y, z


def xyz2rgb(xyz):
    x = xyz[0]
    y = xyz[1]
    z = xyz[2]

    r = 3.063218 * x - 1.393325 * y - 0.475802 * z
    g = -0.969243 * x + 1.875966 * y + 0.041555 * z
    b = 0.067871 * x - 0.228834 * y + 1.069251 * z

    return r, g, b


def anomylize(a, b):
    v = 1.75
    d = v * 1 + 1

    return (
        (v * b[0] + a[0] * 1) / d,
        (v * b[1] + a[1] * 1) / d,
        (v * b[2] + a[2] * 1) / d,
    )


def monochrome(rgb):
    z = rgb[0] * 0.299 + rgb[1] * 0.587 + rgb[2] * 0.114
    return z, z, z


def blindMK(rgb, t):
    gamma = 2.2
    wx = 0.312713
    wy = 0.329016
    wz = 0.358271

    r = rgb[0]
    g = rgb[1]
    b = rgb[2]

    c_rgb = (r**gamma, g**gamma, b**gamma)
    c_xyz = rgb2xyz(c_rgb)

    sum_xyz = sum(c_xyz)

    c_u = 0
    c_v = 0

    if sum_xyz != 0:
        c_u = c_xyz[0] / sum_xyz
        c_v = c_xyz[1] / sum_xyz

    nx = wx * c_xyz[1] / wy
    nz = wz * c_xyz[1] / wy

    d_y = 0

    if c_u < rBlind[t]["cpu"]:
        clm = (rBlind[t]["cpv"] - c_v) / (rBlind[t]["cpu"] - c_u)
    else:
        clm = (c_v - rBlind[t]["cpv"]) / (c_u - rBlind[t]["cpu"])

    clyi = c_v - c_u * clm
    d_u = (rBlind[t]["ayi"] - clyi) / (clm - rBlind[t]["am"])
    d_v = (clm * d_u) + clyi

    s_x = d_u * c_xyz[1] / d_v
    s_y = c_xyz[1]
    s_z = (1 - (d_u + d_v)) * c_xyz[1] / d_v

    s_rgb = xyz2rgb((s_x, s_y, s_z))

    d_x = nx - s_x
    d_z = nz - s_z

    d_rgb = xyz2rgb((d_x, d_y, d_z))

    if d_rgb[0]:
        const = 0 if s_rgb[0] < 0 else 1
        adjr = (const - s_rgb[0]) / d_rgb[0]
    else:
        adjr = 0

    if d_rgb[1]:
        const = 0 if s_rgb[1] < 0 else 1
        adjg = (const - s_rgb[1]) / d_rgb[1]
    else:
        adjg = 0

    if d_rgb[2]:
        const = 0 if s_rgb[2] < 0 else 1
        adjb = (const - s_rgb[2]) / d_rgb[2]
    else:
        adjb = 0

    adjust = max(
        [
            0 if adjr > 1 or adjr < 0 else adjr,
            0 if adjg > 1 or adjg < 0 else adjg,
            0 if adjb > 1 or adjb < 0 else adjb,
        ]
    )

    s_r = s_rgb[0] + (adjust * d_rgb[0])
    s_g = s_rgb[1] + (adjust * d_rgb[1])
    s_b = s_rgb[2] + (adjust * d_rgb[2])

    def z(v):
        if v <= 0:
            const = 0.0
        elif v >= 1:
            const = 1.0
        else:
            const = v ** (1 / gamma)

        return const

    return z(s_r), z(s_g), z(s_b)


fBlind = {
    "Normal": lambda v: v,
    "Protanopia": lambda v: blindMK(v, "protan"),
    "Protanomaly": lambda v: anomylize(v, blindMK(v, "protan")),
    "Deuteranopia": lambda v: blindMK(v, "deutan"),
    "Deuteranomaly": lambda v: anomylize(v, blindMK(v, "deutan")),
    "Tritanopia": lambda v: blindMK(v, "tritan"),
    "Tritanomaly": lambda v: anomylize(v, blindMK(v, "tritan")),
    "Achromatopsia": lambda v: monochrome(v),
    "Achromatomaly": lambda v: anomylize(v, monochrome(v)),
}


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def simulate_image(img_path, colorblind_type):
    """

    :param img_path:

    :param colorblind_type: Type of colourblindness to simulate, can be:

        * 'Normal': Normal vision
        * 'Protanopia': Red-green colorblindness (1% males)
        * 'Protanomaly': Red-green colorblindness (1% males, 0.01% females)
        * 'Deuteranopia': Red-green colorblindness (1% males)
        * 'Deuteranomaly': Red-green colorblindness (most common type: 6% males,
          0.4% females)
        * 'Tritanopia': Blue-yellow colourblindness (<1% males and females)
        * 'Tritanomaly' Blue-yellow colourblindness (0.01% males and females)
        * 'Achromatopsia': Total colourblindness
        * 'Achromatomaly': Total colourblindness

    :return:
    """
    import matplotlib.image as mpimg
    import matplotlib.pyplot as plt

    filter_function = fBlind[colorblind_type]

    img = mpimg.imread(img_path)
    n_rows = img.shape[0]
    n_columns = img.shape[1]

    filtered_img = np.zeros((n_rows, n_columns, 3))

    for r in range(n_rows):
        for c in range(n_columns):
            filtered_img[r, c] = filter_function(img[r, c, 0:3])

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    axes[0].imshow(img)
    axes[1].imshow(filtered_img)

    axes[0].axis("off")
    axes[1].axis("off")

    axes[0].set_title("Normal Vision")
    axes[1].set_title("With " + colorblind_type)

    plt.show()


def colorblind_filter(color, colorblind_type="Deuteranomaly"):
    """
    Transforms an (r,g,b) colour into a simulation of how a person with colourblindnes
    would see that colour.

    :param color: rgb colour tuple to convert

    :param colorblind_type: Type of colourblindness to simulate, can be:

        * 'Normal': Normal vision
        * 'Protanopia': Red-green colorblindness (1% males)
        * 'Protanomaly': Red-green colorblindness (1% males, 0.01% females)
        * 'Deuteranopia': Red-green colorblindness (1% males)
        * 'Deuteranomaly': Red-green colorblindness (most common type: 6% males,
          0.4% females)
        * 'Tritanopia': Blue-yellow colourblindness (<1% males and females)
        * 'Tritanomaly' Blue-yellow colourblindness (0.01% males and females)
        * 'Achromatopsia': Total colourblindness
        * 'Achromatomaly': Total colourblindness

    :return:
    """
    filter_function = fBlind[colorblind_type]

    return filter_function(color)


def simulate_colors(colors, colorblind_type="Deuteranomaly", one_row=None, show=True):
    """
    Simulate the appearance of colors with and without colourblindness.

    :param colors: A list of (r,g,b) colour tuples, with r, g andb floats between 0
        and 1.

    :param colorblind_type: Type of colourblindness to simulate, can be:

        * 'Normal': Normal vision
        * 'Protanopia': Red-green colorblindness (1% males)
        * 'Protanomaly': Red-green colorblindness (1% males, 0.01% females)
        * 'Deuteranopia': Red-green colorblindness (1% males)
        * 'Deuteranomaly': Red-green colorblindness (most common type: 6% males,
          0.4% females)
        * 'Tritanopia': Blue-yellow colourblindness (<1% males and females)
        * 'Tritanomaly' Blue-yellow colourblindness (0.01% males and females)
        * 'Achromatopsia': Total colourblindness
        * 'Achromatomaly': Total colourblindness

    :param one_row: If True display colours on one row, if False as a grid. If
        one_row=None a grid is used when there are more than 8 colours.

    :param show: if True, calls ``plt.show()``.

    :return:
    """
    import matplotlib.pyplot as plt

    from distinctipy import distinctipy

    filtered_colors = [colorblind_filter(color, colorblind_type) for color in colors]

    fig, axes = plt.subplots(1, 2, figsize=(8, 4))

    distinctipy.color_swatch(
        colors, ax=axes[0], one_row=one_row, title="Viewed with Normal Sight"
    )

    distinctipy.color_swatch(
        filtered_colors,
        ax=axes[1],
        one_row=one_row,
        title="Viewed with " + colorblind_type + " Colour Blindness",
    )

    if show:
        plt.show()


def simulate_clusters(
    dataset="s2",
    colorblind_type="Deuteranomaly",
    colorblind_distinct=False,
    show=True,
):
    """
    Simulates the appearance of an example clustering dataset with and without
    colourblindness.

    :param dataset: The dataset to display, the options are:

        * s1, s2, s3, s4: 15 clusters with increasing overlaps from s1 to s4
        * a1: 20 clusters
        * a2: 35 clusters
        * a3: 50 clusters
        * b1: 100 clusters

    :param colorblind_type: Type of colourblindness to simulate, can be:

        * 'Normal': Normal vision
        * 'Protanopia': Red-green colorblindness (1% males)
        * 'Protanomaly': Red-green colorblindness (1% males, 0.01% females)
        * 'Deuteranopia': Red-green colorblindness (1% males)
        * 'Deuteranomaly': Red-green colorblindness (most common type: 6% males,
          0.4% females)
        * 'Tritanopia': Blue-yellow colourblindness (<1% males and females)
        * 'Tritanomaly' Blue-yellow colourblindness (0.01% males and females)
        * 'Achromatopsia': Total colourblindness
        * 'Achromatomaly': Total colourblindness

    :param colorblind_distinct: If True generate colours to be as distinct as possible
        for colorblind_type. Else generate colours that are as distinct as possible for
        normal vision.

    :param show: if True, calls ``plt.show()``.

    :return:
    """
    import matplotlib.pyplot as plt
    import pandas as pd

    from distinctipy import distinctipy

    if dataset not in ("s1", "s2", "s3", "s4", "a1", "a2", "a3", "b1"):
        raise ValueError("dataset must be s1, s2, s3, s4, a1, a2, a3 or b1")

    URL = (
        "https://raw.githubusercontent.com/alan-turing-institute/distinctipy/"
        "main/distinctipy/datasets/"
    )
    df = pd.read_csv(URL + dataset + ".csv")

    if colorblind_distinct:
        orig_colors = distinctipy.get_colors(
            df["cluster"].nunique(), colorblind_type=colorblind_type
        )
    else:
        orig_colors = distinctipy.get_colors(df["cluster"].nunique())

    orig_cmap = distinctipy.get_colormap(orig_colors)

    filtered_colors = [
        colorblind_filter(color, colorblind_type) for color in orig_colors
    ]
    filtered_cmap = distinctipy.get_colormap(filtered_colors)

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.suptitle(str(df["cluster"].nunique()) + " clusters", fontsize=20)

    axes[0].scatter(df["x"], df["y"], c=df["cluster"], cmap=orig_cmap, s=6)
    axes[0].get_xaxis().set_visible(False)
    axes[0].get_yaxis().set_visible(False)
    axes[0].set_title("With Normal Vision")

    axes[1].scatter(df["x"], df["y"], c=df["cluster"], cmap=filtered_cmap, s=6)
    axes[1].get_xaxis().set_visible(False)
    axes[1].get_yaxis().set_visible(False)
    axes[1].set_title("With " + colorblind_type + " Colourblindness")

    if show:
        plt.show()


def _main():
    from distinctipy import distinctipy

    colors = distinctipy.get_colors(36)
    simulate_colors(colors, "Deuteranomaly")


if __name__ == "__main__":
    _main()
