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
        ch = sys.stdin.buffer.read(1)

        if ch == b'\x1b':
            arrow = sys.stdin.buffer.read(2)
            if arrow == b'[A':
                return Keys.UP_KEY
            elif arrow == b'[B':
                return Keys.DOWN_KEY
            elif arrow == b'[C':
                return Keys.RIGHT_KEY
            elif arrow == b'[D':
                return Keys.LEFT_KEY
        if ch == b'\r':
            return Keys.ENTER
    except:
        return ''
    finally:
        reset_terminal()

    return ch.decode()
