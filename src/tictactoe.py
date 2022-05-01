#!/usr/bin/env python3
from enum import Enum, auto
from pyant import Canvas, Pixel, Keys

try:
    c: Canvas = Canvas(24, 8)
except Exception as e:
    print(e)
    Canvas.quit()


class Square(Enum):
    EMPTY = auto()
    NOUGHT = auto()
    CROSS = auto()

    @staticmethod
    def to_char(square: 'Square') -> str:
        if square == Square.EMPTY:
            return ' '
        if square == Square.CROSS:
            return 'X'
        if square == Square.NOUGHT:
            return 'O'


BOARD = 0
TURN = 1
POS = 2
WINNING_SQUARES = 3
GAME_OVER_MSG = 4
MOVE_COUNT = 5


def pixel_to_board_x(x: int) -> int:
    return 7 * x + 5


def pixel_to_board_y(y: int) -> int:
    return 2 * y + 2


def move_up(self: Canvas) -> None:
    self.vars[POS][1] -= 1
    self.vars[POS][1] %= 3


def move_down(self: Canvas) -> None:
    self.vars[POS][1] += 1
    self.vars[POS][1] %= 3


def move_left(self: Canvas) -> None:
    self.vars[POS][0] -= 1
    self.vars[POS][0] %= 3


def move_right(self: Canvas) -> None:
    self.vars[POS][0] += 1
    self.vars[POS][0] %= 3


def put_square(self: Canvas) -> None:
    pos_x, pos_y = self.vars[POS]
    board = self.vars[BOARD]

    if self.vars[WINNING_SQUARES] != None:
        return

    if board[pos_y][pos_x] == Square.EMPTY:
        board[pos_y][pos_x] = self.vars[TURN]
        if self.vars[TURN] == Square.NOUGHT:
            self.vars[TURN] = Square.CROSS
        else:
            self.vars[TURN] = Square.NOUGHT
        self.vars[MOVE_COUNT] += 1

    if self.vars[MOVE_COUNT] == 9:
        self.vars[WINNING_SQUARES] = []

    winner, winning_squares = get_winner(board)
    if winner != Square.EMPTY:
        self.vars[WINNING_SQUARES] = winning_squares


def get_winner(board: list) -> tuple:
    for winning_square in [Square.CROSS, Square.NOUGHT]:
        if board[0][0] == winning_square and board[0][1] == winning_square and board[0][2] == winning_square:
            return winning_square, ([0, 0], [0, 1], [0, 2])
        elif board[1][0] == winning_square and board[1][1] == winning_square and board[1][2] == winning_square:
            return winning_square, ([1, 0], [1, 1], [1, 2])
        elif board[2][0] == winning_square and board[2][1] == winning_square and board[2][2] == winning_square:
            return winning_square, ([2, 0], [2, 1], [2, 2])
        elif board[0][0] == winning_square and board[1][0] == winning_square and board[2][0] == winning_square:
            return winning_square, ([0, 0], [1, 0], [2, 0])
        elif board[0][1] == winning_square and board[1][1] == winning_square and board[2][1] == winning_square:
            return winning_square, ([0, 1], [1, 1], [2, 1])
        elif board[0][2] == winning_square and board[1][2] == winning_square and board[2][2] == winning_square:
            return winning_square, ([0, 2], [1, 2], [2, 2])
        elif board[0][0] == winning_square and board[1][1] == winning_square and board[2][2] == winning_square:
            return winning_square, ([0, 0], [1, 1], [2, 2])
        elif board[0][2] == winning_square and board[1][1] == winning_square and board[2][0] == winning_square:
            return winning_square, ([0, 2], [1, 1], [2, 0])
    return Square.EMPTY, None


def setup(self: Canvas) -> None:
    self.fps = 12

    self.vars[BOARD] = [[Square.EMPTY, Square.EMPTY, Square.EMPTY] for _ in range(3)]
    self.vars[TURN] = Square.CROSS
    self.vars[POS] = [1, 1]
    self.vars[WINNING_SQUARES] = None
    self.vars[GAME_OVER_MSG] = None
    self.vars[MOVE_COUNT] = 0

    self.on_click('w', move_up)
    self.on_click('s', move_down)
    self.on_click('a', move_left)
    self.on_click('d', move_right)
    self.on_click(Keys.ENTER, put_square)


class Colors:
    BLACK = Pixel.hex_to_xterm_color(0x000000)
    BLUE = Pixel.hex_to_xterm_color(0x1234dd)
    RED = Pixel.hex_to_xterm_color(0xdd1234)
    WHITE = Pixel.empty_color()
    YELLOW = Pixel.hex_to_xterm_color(0xffff12)
    GRAY = Pixel.hex_to_xterm_color(0xcacaca)


def draw(self: Canvas) -> None:
    board = self.vars[BOARD]
    pos = self.vars[POS]

    pos_x = pixel_to_board_x(pos[0])
    pos_y = pixel_to_board_y(pos[1])

    if self.vars[GAME_OVER_MSG] != None:
        print(self.vars[GAME_OVER_MSG])
        self.quit()

    self.set_all_pixels(Pixel(' ', Colors.BLACK, Colors.WHITE))

    for i in range(self.width):
        self.set_pixel(i, 0, Pixel(' ', Colors.BLACK, Colors.BLUE))
    for i in range(self.height):
        self.set_pixel(0, i, Pixel(' ', Colors.BLACK, Colors.BLUE))
        self.set_pixel(1, i, Pixel(' ', Colors.BLACK, Colors.BLUE))
        self.set_pixel(2, i, Pixel(' ', Colors.BLACK, Colors.BLUE))

    for i in range(3):
        self.get_pixel(pixel_to_board_x(i), 0).character = str(i + 1)
    for i in range(3):
        self.get_pixel(1, pixel_to_board_y(i)).character = chr(i + ord('a'))

    for i in range(3):
        for j in range(3):
            self.get_pixel(pixel_to_board_x(i), pixel_to_board_y(j)).character = Square.to_char(board[j][i])

    self.set_pixel(pos_x - 1, pos_y, Pixel('[', Colors.RED, Colors.WHITE))
    self.set_pixel(pos_x + 1, pos_y, Pixel(']', Colors.RED, Colors.WHITE))
    if board[pos[1]][pos[0]] == Square.EMPTY:
        self.set_pixel(pos_x, pos_y, Pixel(Square.to_char(self.vars[TURN]), Colors.GRAY, Colors.WHITE))

    if self.vars[WINNING_SQUARES] != None:
        winner = Square.EMPTY
        for square_y, square_x in self.vars[WINNING_SQUARES]:
            pixel = self.get_pixel(pixel_to_board_x(square_x), pixel_to_board_y(square_y))
            pixel.background = Colors.YELLOW
            winner = pixel.character
        if winner == Square.EMPTY:
            self.vars[GAME_OVER_MSG] = 'Game is a draw.'
        else:
            self.vars[GAME_OVER_MSG] = f'Winner is {winner}'


c.play(setup, draw)
