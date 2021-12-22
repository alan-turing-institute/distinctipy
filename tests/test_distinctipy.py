import distinctipy


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


def test_rng():
    """Assert same colours returned if rng state give, and not if it's not given"""
    assert distinctipy.get_colors(10, rng=123) == distinctipy.get_colors(10, rng=123)
    assert distinctipy.get_colors(10) != distinctipy.get_colors(10)


def test_colors_are_floats():
    """Check that random colors dont contain integers"""
    colors1 = distinctipy.get_colors(10)
    colors2 = distinctipy.get_colors(10, exclude_colors=colors1)
    for color in colors1 + colors2:
        r, g, b = color
        assert isinstance(r, float)
        assert isinstance(g, float)
        assert isinstance(b, float)


def test_constants_are_floats():
    """Check that known color constants dont have integers in them"""
    from distinctipy import colorsets

    def _assert_colors_are_floats(colors):
        for color in colors:
            r, g, b = color
            assert isinstance(r, float)
            assert isinstance(g, float)
            assert isinstance(b, float)

    for name in colorsets.list_colorsets():
        colors = colorsets.get_colors(name)
        _assert_colors_are_floats(colors)
    _assert_colors_are_floats(distinctipy.CORNERS)
    _assert_colors_are_floats(distinctipy.POINTS_OF_INTEREST)


def test_distinct_color_with_colorblind():
    colorblind_types = list(distinctipy.colorblind.fBlind)
    for colorblind_type in colorblind_types:
        pass


def test_ensure_rng():
    import random
    from distinctipy.distinctipy import _ensure_rng
    assert _ensure_rng(1).randint(0, 1000) == 137
    assert _ensure_rng(1.3).randint(0, 1000) == 57
    rng = random.Random()
    assert _ensure_rng(rng) is rng
    assert _ensure_rng(1) is not rng
    assert _ensure_rng(None) is not rng
    assert _ensure_rng(None) is random._inst
