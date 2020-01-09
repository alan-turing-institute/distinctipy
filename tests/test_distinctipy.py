from distinctipy import distinctipy


def test_get_random_color():
    """Assert all r,g,b components are between 0 and 1"""
    color = distinctipy.get_random_color()
    assert all([x >= 0 and x <= 1 for x in color])

