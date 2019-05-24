import pandas as pd
import matplotlib.pyplot as plt
from distinctipy import distinctipy
import os


def plot_example(dataset='a3'):
    """
    Displays comparisons of distinctipy colormaps with the built-in matplotlib colormaps Set1, tab20 and nipy-spectral,
    using example clustering datasets from P. Fränti and S. Sieranoja (http://cs.joensuu.fi/sipu/datasets/).

    :param dataset: The dataset to display, the options are:
        * s1, s2, s3, s4: 15 clusters with increasing overlaps from s1 to s4
        * a1: 20 clusters
        * a2: 35 clusters
        * a3: 50 clusters
        * b1: 100 clusters

    :type dataset: str

    :return:
    """

    if dataset not in ('s1', 's2', 's3', 's4', 'a1','a2', 'a3', 'b1'):
        raise ValueError('dataset must be s1, s2, s3, s4, a1, a2, a3 or b1')

    URL = "https://raw.githubusercontent.com/alan-turing-institute/distinctipy/master/distinctipy/datasets/"
    df = pd.read_csv(URL + dataset + '.csv')

    colors = distinctipy.get_colors(df['cluster'].nunique(),
                                    exclude_colors=[(1, 1, 1), (0, 0, 0)], return_excluded=False)

    cmap = distinctipy.get_colormap(colors)

    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.suptitle(str(df['cluster'].nunique()) + ' clusters', fontsize=20)

    axes[0, 0].scatter(df['x'], df['y'], c=df['cluster'], cmap=cmap, s=6)
    axes[0, 0].get_xaxis().set_visible(False)
    axes[0, 0].get_yaxis().set_visible(False)
    axes[0, 0].set_title('distinctipy')

    axes[0, 1].scatter(df['x'], df['y'], c=df['cluster'], cmap='Set1', s=6)
    axes[0, 1].get_xaxis().set_visible(False)
    axes[0, 1].get_yaxis().set_visible(False)
    axes[0, 1].set_title('Set1')

    axes[1, 0].scatter(df['x'], df['y'], c=df['cluster'], cmap='tab20', s=6)
    axes[1, 0].get_xaxis().set_visible(False)
    axes[1, 0].get_yaxis().set_visible(False)
    axes[1, 0].set_title('tab20')

    axes[1, 1].scatter(df['x'], df['y'], c=df['cluster'], cmap='nipy_spectral', s=6)
    axes[1, 1].get_xaxis().set_visible(False)
    axes[1, 1].get_yaxis().set_visible(False)
    axes[1, 1].set_title('nipy_spectral')

    plt.show()
