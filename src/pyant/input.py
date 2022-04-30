from enum import Enum, auto
import tty
import sys
import termios

fd = sys.stdin.fileno()
INITIAL_STATE = termios.tcgetattr(fd)


def reset_terminal():
    termios.tcsetattr(fd, termios.TCSADRAIN, INITIAL_STATE)


class Keys(Enum):
    ESCAPE = auto()
    UP_KEY = auto()
    DOWN_KEY = auto()
    LEFT_KEY = auto()
    RIGHT_KEY = auto()
    ENTER = auto()


def getch():
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)

        if ch == '\x1b':
            arrow = ch + sys.stdin.read(2)
            if arrow == '\x1b[A':
                return Keys.UP_KEY
            elif arrow == '\x1b[B':
                return Keys.DOWN_KEY
            elif arrow == '\x1b[C':
                return Keys.RIGHT_KEY
            elif arrow == '\x1b[D':
                return Keys.LEFT_KEY
        if ch == '\r':
            return Keys.ENTER
    except:
        return ''
    finally:
        reset_terminal()

    return ch
