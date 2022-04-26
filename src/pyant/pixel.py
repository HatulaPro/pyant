from numpy import character
import xtermcolor


class Pixel:
    _character: str
    foreground: int
    background: int

    def __init__(self, character: str, foreground: int, background: int) -> None:
        # if not isinstance(character, str):
        #     raise TypeError('Character must be a string.')
        # if len(character) != 1:
        #     raise ValueError('Character must be a string of length one.')

        if not isinstance(foreground, int):
            raise TypeError('Foreground must be an integer.')
        if not isinstance(background, int):
            raise TypeError('Background must be an integer.')

        self.character = character
        self.foreground = foreground
        self.background = background

    @property
    def character(self) -> str:
        return self._character

    @character.setter
    def character(self, character: str) -> str:
        if not isinstance(character, str):
            raise TypeError('Character must be a string.')
        if len(character) != 1:
            raise ValueError('Character must be a string of length one.')
        self._character = character

    def _get_show_string(self) -> str:
        return f'\033[38;5;{self.foreground}m\033[48;5;{self.background}m{self.character}\033[m'

    @staticmethod
    def hex_to_xterm_color(hex_color: int):
        return xtermcolor.ColorMap.XTermColorMap().convert(hex_color)[0]
