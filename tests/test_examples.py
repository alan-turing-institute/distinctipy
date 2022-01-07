import distinctipy


def require_modules(modnames):
    """
    Given a list of module names, skip the test if any of them dont exist
    """
    import importlib

    import pytest

    for modname in modnames:
        try:
            importlib.import_module(modname)
        except (ImportError, ModuleNotFoundError):
            pytest.skip("test requires {}".format(modname))


def test_compare_clusters():
    require_modules(["matplotlib"])
    distinctipy.examples.compare_clusters(show=False)


def test_compare_colors():
    require_modules(["matplotlib"])
    distinctipy.examples.compare_colors(show=False)


def test_color_swatch():
    require_modules(["matplotlib"])
    import matplotlib.pyplot as plt

    ax = plt.gca()
    colors = distinctipy.get_colors(10)
    distinctipy.distinctipy.color_swatch(colors, ax=ax)


def test_simulate_clusters():
    require_modules(["matplotlib", "pandas"])
    distinctipy.colorblind.simulate_clusters(show=False)


def test_simulate_colors():
    require_modules(["matplotlib"])
    colors = distinctipy.get_colors(10)
    distinctipy.colorblind.simulate_colors(colors, show=False)
