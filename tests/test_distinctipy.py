from distinctipy import distinctipy


def test_get_random_color():
    color = distinctipy.get_random_color()
    assert all([x >= 0 and x <= 1 for x in color])
