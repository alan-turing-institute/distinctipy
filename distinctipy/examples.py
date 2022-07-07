import numpy as np

from . import distinctipy


def compare_clusters(dataset="a3", compare_with="tab20", show=True):
    """
    Displays comparisons of distinctipy colormaps with built-in matplotlib colormaps
    using example clustering datasets from P. Fränti and S. Sieranoja
    (http://cs.joensuu.fi/sipu/datasets/).

    :param dataset: The dataset to display, the options are:

        * s1, s2, s3, s4: 15 clusters with increasing overlaps from s1 to s4
        * a1: 20 clusters
        * a2: 35 clusters
        * a3: 50 clusters
        * b1: 100 clusters

    :param compare_with: The name of a matplotlib cmap to compare distinctipy with.

    :type dataset: str

    :type compare_with: str

    :return:
    """
    import matplotlib.pyplot as plt
    import pandas as pd

    if dataset not in ("s1", "s2", "s3", "s4", "a1", "a2", "a3", "b1"):
        raise ValueError("dataset must be s1, s2, s3, s4, a1, a2, a3 or b1")

    URL = (
        "https://raw.githubusercontent.com/alan-turing-institute/distinctipy/"
        "main/distinctipy/datasets/"
    )
    df = pd.read_csv(URL + dataset + ".csv")

    colors = distinctipy.get_colors(
        df["cluster"].nunique(),
        exclude_colors=[(1, 1, 1), (0, 0, 0)],
        return_excluded=False,
    )

    cmap = distinctipy.get_colormap(colors)

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.suptitle(str(df["cluster"].nunique()) + " clusters", fontsize=20)

    axes[0].scatter(df["x"], df["y"], c=df["cluster"], cmap=cmap, s=6)
    axes[0].get_xaxis().set_visible(False)
    axes[0].get_yaxis().set_visible(False)
    axes[0].set_title("distinctipy")

    axes[1].scatter(df["x"], df["y"], c=df["cluster"], cmap=compare_with, s=6)
    axes[1].get_xaxis().set_visible(False)
    axes[1].get_yaxis().set_visible(False)
    axes[1].set_title(compare_with)

    if show:
        plt.show()


def compare_colors(N=36, compare_with="tab20", show=True):
    """
    Compare colour swatches for distinctipy and a given matplotlib colormap for N
    colours.

    :param N: Number of colours to generate

    :param compare_with: str representing name of a built-in matplotlib colormap

    :return:
    """
    import matplotlib.cm
    import matplotlib.colors
    import matplotlib.pyplot as plt

    colors_distinctipy = distinctipy.get_colors(
        N, exclude_colors=[(1, 1, 1), (0, 0, 0)], return_excluded=False
    )

    cmap = matplotlib.cm.get_cmap(compare_with)
    if type(cmap) is matplotlib.colors.ListedColormap:
        colors_compare = [cmap.colors[i % len(cmap.colors)] for i in range(N)]

    else:
        colors_compare = [cmap(i) for i in np.linspace(0, 1, N)]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    distinctipy.color_swatch(colors_distinctipy, ax=axes[0], title="distinctipy")
    distinctipy.color_swatch(colors_compare, ax=axes[1], title=compare_with)

    if show:
        plt.show()
