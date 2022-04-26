import os
import sys
import time
from tkinter import W

from pyant.pixel import Pixel

TERMINAL_DIMENSIONS = os.get_terminal_size()


class Canvas:
    _width: int
    _height: int
    _pixels: list[Pixel]
    _fps: int
    _clear_on_finish: bool

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self._pixels = [Pixel(' ', Pixel.hex_to_xterm_color(0x000000), Pixel.hex_to_xterm_color(0xffffff)) for _ in range(width * height)]
        self._fps = 60
        self.clear_on_finish = True
        Canvas._hide_cursor()
        Canvas._save_cursor_position()

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, w: int) -> None:
        if not isinstance(w, int):
            raise TypeError('Canvas width must be an integer.')

        if w > TERMINAL_DIMENSIONS.columns:
            raise TypeError(f'Width is too big. The terminal is only {TERMINAL_DIMENSIONS.columns} columns wide.')
        if w < 0:
            raise TypeError('Width must be a positive integer.')

        self._width = w

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, h: int) -> None:
        if not isinstance(h, int):
            raise TypeError('Canvas height must be an integer.')

        if h > TERMINAL_DIMENSIONS.lines:
            raise TypeError(f'Height is too big. The terminal is only {TERMINAL_DIMENSIONS.lines} lines high.')
        if h < 0:
            raise TypeError('Height must be a positive integer.')

        self._height = h

    @property
    def clear_on_finish(self) -> bool:
        return self._clear_on_finish

    @clear_on_finish.setter
    def clear_on_finish(self, clear_on_finish: bool) -> None:
        if not isinstance(clear_on_finish, bool):
            raise TypeError('Value must be a boolean.')

        self._clear_on_finish = clear_on_finish

    def __del__(self) -> None:
        Canvas._show_cursor()
        if(self.clear_on_finish):
            Canvas._restore_cursor_position()

    def draw(self) -> None:
        Canvas._restore_cursor_position()
        for i in range(self.height):
            for j in range(self.width):
                sys.stdout.write(self._pixels[i * self.width + j]._get_show_string())
            sys.stdout.write('\n')
        time.sleep(1 / self._fps)

    def get_pixel(self, x: int, y: int) -> Pixel:
        return self._pixels[y * self.width + x]

    def set_pixel(self, value: Pixel, x: int, y: int) -> None:
        self._pixels[y * self.width + x] = value

    @staticmethod
    def _save_cursor_position() -> None:
        sys.stdout.write('\33[s')

    @staticmethod
    def _restore_cursor_position() -> None:
        sys.stdout.write('\33[u')

    @staticmethod
    def _hide_cursor() -> None:
        sys.stdout.write('\33[?25l')

    @staticmethod
    def _show_cursor() -> None:
        sys.stdout.write('\33[?25h')
