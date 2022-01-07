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
    assert distinctipy.get_text_color((1, 1, 1)) == (0, 0, 0)


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


def test_invert_colors():
    from distinctipy.distinctipy import INTERIOR, get_rgb256, invert_colors

    inverted = invert_colors(INTERIOR)
    result = [get_rgb256(c) for c in inverted]
    expected = [
        (255, 255, 255),
        (0, 255, 255),
        (255, 255, 255),
        (255, 0, 255),
        (255, 255, 255),
        (255, 255, 0),
        (255, 255, 255),
    ]
    assert expected == result


def test_colorblind_options():
    from distinctipy.distinctipy import BLACK, WHITE, get_rgb256

    colorblind_types = sorted(distinctipy.colorblind.fBlind)
    results = []
    for colorblind_type in colorblind_types:
        colors = distinctipy.get_colors(
            5, rng=15662713, colorblind_type=colorblind_type
        )
        exclude = colors + [BLACK, WHITE]

        new_color = distinctipy.distinct_color(
            exclude, colorblind_type=colorblind_type, rng=15662713
        )

        info = {
            "type": colorblind_type,
            "colors": [get_rgb256(c) for c in colors],
            "new_colors": get_rgb256(new_color),
        }
        results.append(info)
    expected = [
        {
            "colors": [
                (9, 157, 230),
                (239, 13, 3),
                (252, 185, 22),
                (0, 0, 255),
                (17, 253, 248),
            ],
            "new_colors": (255, 0, 255),
            "type": "Achromatomaly",
        },
        {
            "colors": [
                (128, 128, 128),
                (15, 67, 174),
                (144, 236, 86),
                (55, 237, 36),
                (69, 104, 124),
            ],
            "new_colors": (35, 8, 149),
            "type": "Achromatopsia",
        },
        {
            "colors": [
                (0, 128, 255),
                (255, 128, 0),
                (178, 25, 130),
                (28, 211, 171),
                (211, 234, 6),
            ],
            "new_colors": (167, 2, 0),
            "type": "Deuteranomaly",
        },
        {
            "colors": [
                (208, 38, 250),
                (240, 136, 18),
                (120, 163, 170),
                (89, 62, 107),
                (202, 224, 6),
            ],
            "new_colors": (162, 46, 2),
            "type": "Deuteranopia",
        },
        {
            "colors": [
                (0, 255, 0),
                (255, 0, 255),
                (0, 128, 255),
                (255, 128, 0),
                (128, 191, 128),
            ],
            "new_colors": (72, 3, 167),
            "type": "Normal",
        },
        {
            "colors": [
                (34, 109, 250),
                (145, 179, 14),
                (255, 0, 128),
                (1, 223, 183),
                (65, 2, 163),
            ],
            "new_colors": (208, 253, 7),
            "type": "Protanomaly",
        },
        {
            "colors": [
                (151, 86, 241),
                (21, 191, 12),
                (12, 176, 191),
                (60, 70, 115),
                (222, 233, 113),
            ],
            "new_colors": (18, 96, 5),
            "type": "Protanopia",
        },
        {
            "colors": [
                (1, 162, 214),
                (255, 69, 91),
                (89, 108, 21),
                (109, 246, 18),
                (158, 3, 8),
            ],
            "new_colors": (226, 132, 249),
            "type": "Tritanomaly",
        },
        {
            "colors": [
                (1, 162, 214),
                (255, 69, 91),
                (188, 142, 244),
                (113, 46, 164),
                (26, 250, 133),
            ],
            "new_colors": (167, 2, 0),
            "type": "Tritanopia",
        },
    ]
    assert results == expected


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
