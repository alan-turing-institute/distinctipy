from distinctipy import distinctipy


def is_valid_color(color):
    """Returns True is color is length 3 (r,g,b) with each element between
    0 and 1."""
    return len(color) == 3 and all([x >= 0 and x <= 1 for x in color])


def test_get_random_color():
    """Assert all r,g,b components are between 0 and 1"""
    color = distinctipy.get_random_color()
    assert is_valid_color(color)


def test_distinct_color():
    """Assert distinct_color returns black when told to generate a colour as
    distinct as possible to white."""
    color = distinctipy.distinct_color([(1, 1, 1)])
    assert color == (0, 0, 0)


def test_get_colors():
    """Assert get_colors returns the number of colours expected, and that each
    colour returned is valid."""
    colors = distinctipy.get_colors(5)
    assert len(colors) == 5 and all([is_valid_color(c) for c in colors])


def test_color_distance():
    """Assert colour distance returns larger values for more
    distinct colours."""
    d1 = distinctipy.color_distance((1, 1, 1), (0, 0, 0))
    d2 = distinctipy.color_distance((0.5, 0.5, 0.5), (0, 0, 0))
    assert d1 > d2


def test_text_color():
    """Assert suggested text colour for black background is white."""
    assert distinctipy.get_text_color((0, 0, 0)) == (1, 1, 1)
