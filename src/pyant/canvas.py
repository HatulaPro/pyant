import os
import sys
import threading
import time
from pyant.input import getch, reset_terminal
from pyant.pixel import Pixel

TERMINAL_DIMENSIONS = os.get_terminal_size()


class Canvas:
    _width: int
    _height: int
    _pixels: list[Pixel]
    _fps: int
    _clear_on_finish: bool
    _done: bool

    _click_listeners: dict

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self._pixels = [Pixel(' ', Pixel.hex_to_xterm_color(0x000000), Pixel.hex_to_xterm_color(0xffffff)) for _ in range(width * height)]
        self._fps = 60
        self._clear_on_finish = True
        self._done = False

        self._click_listeners = {}
        self._begin_click_listener()

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

    @property
    def fps(self) -> bool:
        return self._fps

    @fps.setter
    def fps(self, fps: bool) -> None:
        if not isinstance(fps, int):
            raise TypeError('New FPS must be an integer.')
        if fps < 1:
            raise TypeError('New FPS must be greater than or equal to one.')

        self._fps = fps

    def __del__(self) -> None:
        if self._clear_on_finish:
            Canvas._restore_cursor_position()
        self._done = True

    @staticmethod
    def quit():
        reset_terminal()
        os._exit(0)

    def draw(self) -> None:
        Canvas._restore_cursor_position()
        for i in range(self.height):
            for j in range(self.width):
                sys.stdout.write(self._pixels[i * self.width + j]._get_show_string())
            sys.stdout.write('\r\n')
        time.sleep(1 / self._fps)

    def get_pixel(self, x: int, y: int) -> Pixel:
        return self._pixels[y * self.width + x]

    def set_pixel(self, x: int, y: int, value: Pixel, square_mode: bool = False) -> None:
        if square_mode:
            self._pixels[y * self.width + (x * 2)] = value
            self._pixels[y * self.width + (x * 2 + 1)] = value
        else:
            self._pixels[y * self.width + x] = value

    def background(self, color: int) -> None:
        for pixel in self._pixels:
            pixel.background = color

    def set_all_pixels(self, pixel: Pixel) -> None:
        for p in self._pixels:
            p.background = pixel.background
            p.foreground = pixel.foreground
            p._character = pixel.character

    def _begin_click_listener(self) -> None:

        def click_listener(self: Canvas) -> None:
            while not self._done:
                x = getch()
                if x in self._click_listeners:
                    self._click_listeners[x](self)
                if x == '\x03':
                    print('^C')
                    Canvas.quit()

        t = threading.Thread(target=click_listener, name='click listener', args=(self, ))
        t.daemon = True
        t.start()

    def on_click(self, key, func) -> None:
        self._click_listeners[key] = func

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
