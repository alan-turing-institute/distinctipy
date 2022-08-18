import unittest

from distinctipy.color import Color


def check_equal(tuple1, tuple2) -> bool:
    return all(x == y for x, y in zip(tuple1, tuple2))


class TestBlobManager(unittest.TestCase):

    def test_color1(self):
        color = Color.get_color(rng=123123).tuple()
        expected = (0.9409962223692785, 0.9108596801202742, 0.996284123178982)
        self.assertTrue(check_equal(color, expected))

    def test_color2(self):
        color = Color.get_color(rng=54321).tuple()
        expected = (0.48866987066258627, 0.9882259597584993, 0.24456828827706578)
        self.assertTrue(check_equal(color, expected))

    def test_get_colors1(self):
        colors = Color.get_colors(3, rng=123123)
        expected = [
            (0.0, 1.0, 0.0),
            (1.0, 0.0, 1.0),
            (0.0, 0.5, 1.0)
        ]
        for i, color in enumerate(colors):
            self.assertTrue(check_equal(color.tuple(), expected[i]))

    def test_get_colors2(self):
        colors = Color.get_colors(3, rng=123123, pastel_factor=0.3)
        expected = [
            (0.3550144248699979, 0.25428377375481004, 0.9985706133743355),
            (0.24250062735618416, 0.9839177165862908, 0.2535440877869681),
            (0.9288861441826036, 0.3166081385307568, 0.26839081842829504)
        ]
        for i, color in enumerate(colors):
            self.assertTrue(check_equal(color.tuple(), expected[i]))

    def test_invert(self):
        color = Color.get_color(rng=54321).invert().tuple()
        expected = (1.0, 0.0, 1.0)
        self.assertTrue(check_equal(color, expected))

    def test_cv2_1(self):
        color = Color.get_color(rng=54321, pastel_factor=0.3).cv2()
        expected = (107, 253, 155)
        self.assertTrue(check_equal(color, expected))

    def test_cv2_2(self):
        color = Color.get_color(rng=1234, pastel_factor=0.1).cv2()
        expected = (25, 125, 247)
        self.assertTrue(check_equal(color, expected))

    def test_distance(self):
        color1 = Color.get_color(rng=1234, pastel_factor=0.1)
        color2 = Color.get_color(rng=4321, pastel_factor=0.3)
        dist = color1.distance(color2)
        self.assertEqual(0.8831609432987555, dist)

    def test_text_color(self):
        color = Color.get_color(rng=999, pastel_factor=0.1)
        text_color = color.text_color().tuple()
        self.assertTrue(check_equal(text_color, (1.0, 1.0, 1.0)))

    def test_from_rgb8(self):
        color = Color.from_rgb8((255, 0, 127)).default_tuple()
        expected = (1.0, 0.0, 0.4980392156862745)
        self.assertTrue(check_equal(color, expected))
