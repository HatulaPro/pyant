import os
import sys
import time

TERMINAL_DIMENSIONS = os.get_terminal_size()


class Canvas:
    width: int
    height: int
    _pixels: list[int]
    _fps: int

    def __init__(self, width: int, height: int) -> None:
        if not isinstance(width, int):
            raise TypeError('Canvas width must be an integer.')
        if not isinstance(height, int):
            raise TypeError('Canvas height must be an integer.')

        if width > TERMINAL_DIMENSIONS.columns:
            raise TypeError(f'Width is too big. The terminal is only {TERMINAL_DIMENSIONS.columns} columns wide.')
        if width < 0:
            raise TypeError('Width must be a positive integer.')
        if height > TERMINAL_DIMENSIONS.lines:
            raise TypeError(f'Height is too big. The terminal is only {TERMINAL_DIMENSIONS.lines} lines high.')
        if height < 0:
            raise TypeError('Height must be a positive integer.')

        self.width = width
        self.height = height
        # TODO: think of a better way to represent pixels
        self._pixels = ['X'] * (width * height)
        self._fps = 60
        Canvas._hide_cursor()
        Canvas._save_cursor_position()

    def __del__(self) -> None:
        Canvas._show_cursor()
        Canvas._restore_cursor_position()

    def draw(self) -> None:
        Canvas._restore_cursor_position()
        for i in range(self.height):
            for j in range(self.width):
                sys.stdout.write(self._pixels[i * self.width + j])
            sys.stdout.write('\n')
        time.sleep(1 / self._fps)

    def get_pixel(self, x: int, y: int) -> str:
        return self._pixels[y * self.width + x]

    def set_pixel(self, value: str, x: int, y: int) -> None:
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
