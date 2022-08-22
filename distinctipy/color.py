from typing import Tuple, List
from enum import IntEnum
from numbers import Number

from .distinctipy import *


class ColorOrder(IntEnum):
    RGB = 1  # Default of the library
    BGR = 2


class DataType(IntEnum):
    FLOAT = 1  # Default of the library, 0..1 float
    INT8 = 2  # Used by cv2, 0..255 int
    INT16 = 3  # 0..65535 int


class Color:
    colors: Tuple[Number, Number, Number]

    _color_order: ColorOrder = ColorOrder.RGB
    _data_type: DataType = DataType.FLOAT

    def __init__(self, colors: Tuple[Number, Number, Number],
                 color_order: ColorOrder = ColorOrder.RGB,
                 data_type: DataType = DataType.FLOAT):

        self.colors = colors
        self._color_order = color_order
        self._data_type = data_type

    @classmethod
    def from_rgb8(rgb8: Tuple[int, int, int]) -> 'Color':
        return Color(rgb8, color_order=ColorOrder.RGB, data_type=DataType.INT8)

    @classmethod
    def from_bgr8(bgr8: Tuple[int, int, int]) -> 'Color':
        return Color(bgr8, color_order=ColorOrder.BGR, data_type=DataType.INT8)

    @classmethod
    def from_rgb_float(rgb_float: Tuple[float, float, float]) -> 'Color':
        return Color(rgb_float, color_order=ColorOrder.RGB, data_type=DataType.FLOAT)

    @classmethod
    def from_bgr_float(bgr_float: Tuple[float, float, float]) -> 'Color':
        return Color(bgr_float, color_order=ColorOrder.BGR, data_type=DataType.FLOAT)

    @classmethod
    def get_color(pastel_factor: float = 0, rng=None) -> 'Color':
        return Color(get_random_color(pastel_factor, rng))

    @classmethod
    def get_colors(n_colors,
                   exclude_colors=None,
                   return_excluded=False,
                   pastel_factor=0,
                   n_attempts=1000,
                   colorblind_type=None,
                   rng=None) -> List['Color']:
        colors = get_colors(
            n_colors,
            exclude_colors,
            return_excluded,
            pastel_factor,
            n_attempts,
            colorblind_type,
            rng
        )
        return [Color(color) for color in colors]

    def _reverse_color_order(self):
        """
        BGR -> RGB or RGB -> BGR
        """
        self.colors = (self.colors[2], self.colors[1], self.colors[0])

    def bgr(self) -> 'Color':
        if self._color_order == ColorOrder.BGR:
            return self  # Already in BGR
        self._reverse_color_order()
        self._color_order = ColorOrder.BGR
        return self

    def rgb(self) -> 'Color':
        """
        Convert color order to RGB
        """
        if self._color_order == ColorOrder.RGB:
            return self  # Already in RGB
        self._reverse_color_order()
        self._color_order = ColorOrder.RGB
        return self

    def float(self) -> 'Color':
        """
        Convert color values to float [0.0,1.0]
        """
        if self._data_type == DataType.FLOAT:
            return self  # Already in FLOAT

        if self._data_type == DataType.INT8:
            self.colors = (
                self.colors[0] / 255,
                self.colors[1] / 255,
                self.colors[2] / 255,
            )
        elif self._data_type == DataType.INT16:
            self.colors = (
                self.colors[0] / 65535,
                self.colors[1] / 65535,
                self.colors[2] / 65535,
            )
        self._data_type = DataType.FLOAT
        return self

    def type(self, data_type: DataType) -> 'Color':
        if data_type == self._data_type:
            return self

        self.float()  # First convert to FLOAT

        if data_type == DataType.INT8:
            self.colors = (
                round(self.colors[0] * 255),
                round(self.colors[1] * 255),
                round(self.colors[2] * 255),
            )
        elif data_type == DataType.INT16:
            self.colors = (
                round(self.colors[0] * 65535),
                round(self.colors[1] * 65535),
                round(self.colors[2] * 65535),
            )

        self._data_type = data_type
        return self

    def tuple(self) -> Tuple[Number, Number, Number]:
        return self.colors

    def cv2(self) -> Tuple[int, int, int]:
        return self.copy().bgr().type(DataType.INT8).tuple()

    def hex(self) -> str:
        return get_hex(self.default_tuple())

    def text_color(self, threshold=0.6) -> 'Color':
        return Color(get_text_color(self.default_tuple(), threshold))

    def distance(self, other: 'Color') -> float:
        return color_distance(
            self.default_tuple(),
            other.default_tuple()
        )

    def invert(self) -> 'Color':
        return Color(invert_color(self.default_tuple()))

    def copy(self) -> 'Color':
        return Color(self.colors, self._color_order, self._data_type)

    def default(self) -> 'Color':
        return self.copy().rgb().float()

    def default_tuple(self) -> Tuple[float, float, float]:
        return self.default().tuple()
