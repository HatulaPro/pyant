#!/usr/bin/env python3
import os
import random
from pyant import Canvas, Pixel

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

c = Canvas(32, 16)
# c.clear_on_finish = False
c.fps = 4

snake = [[1, 1], [1, 2], [1, 3]]
treat = [0, 0]


def retreat():
    global treat
    treat[0] = random.randint(0, c.width / 2)
    treat[1] = random.randint(0, c.height)


retreat()
moving_direction = RIGHT
lock_changes = False


def locker(func):
    def inner(arg):
        global lock_changes
        if not lock_changes:
            lock_changes = True
            func(arg)
            lock_changes = False
    return inner


@locker
def move_left(c: Canvas):
    global moving_direction
    if moving_direction != RIGHT:
        moving_direction = LEFT


@locker
def move_right(c: Canvas):
    global moving_direction
    if moving_direction != LEFT:
        moving_direction = RIGHT


@locker
def move_up(c: Canvas):
    global moving_direction
    if moving_direction != DOWN:
        moving_direction = UP


@locker
def move_down(c: Canvas):
    global moving_direction
    if moving_direction != UP:
        moving_direction = DOWN


c.on_click('a', move_left)
c.on_click('s', move_down)
c.on_click('w', move_up)
c.on_click('d', move_right)

while not c._done:
    head = snake[-1]
    c.set_all_pixels(Pixel(' ', Pixel.hex_to_xterm_color(0x00ff00), Pixel.hex_to_xterm_color(0x40ff60)))

    head_x, head_y = head
    lock_changes = True

    # Moving the head
    new_head_x = head_x
    new_head_y = head_y
    if moving_direction == DOWN:
        new_head_y += 1
    elif moving_direction == UP:
        new_head_y -= 1
    elif moving_direction == RIGHT:
        new_head_x += 1
    elif moving_direction == LEFT:
        new_head_x -= 1

    if new_head_x == treat[0] and new_head_y == treat[1]:
        snake.append([treat[0], treat[1]])
        retreat()
    else:
        for i in range(len(snake) - 1):
            snake[i][0], snake[i][1] = snake[i + 1]
            if new_head_x == snake[i][0] and new_head_y == snake[i][1]:
                Canvas.quit()
        snake[-2] = [head_x, head_y]
        snake[-1] = [new_head_x, new_head_y]

    lock_changes = False

    if new_head_x < 0 or new_head_x * 2 >= c.width or new_head_y < 0 or new_head_y >= c.height:
        Canvas.quit()

    for [x, y] in snake[:-1]:
        c.set_pixel(x, y, Pixel(' ', Pixel.hex_to_xterm_color(0x00ff00), Pixel.hex_to_xterm_color(0xf5e642)), square_mode=True)
    c.set_pixel(new_head_x, new_head_y, Pixel(' ', Pixel.hex_to_xterm_color(0x00ff00), Pixel.hex_to_xterm_color(0xffae21)), square_mode=True)

    c.set_pixel(treat[0], treat[1], Pixel(' ', Pixel.hex_to_xterm_color(0x00ff00), Pixel.hex_to_xterm_color(0xff0000)), square_mode=True)
    c.draw()
