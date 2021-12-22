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
            pytest.skip('test requires {}'.format(modname))


def test_compare_clusters():
    require_modules(['matplotlib'])
    distinctipy.examples.compare_clusters(show=False)


def test_compare_colors():
    require_modules(['matplotlib'])
    distinctipy.compare_colors(show=False)
