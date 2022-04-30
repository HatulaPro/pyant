#!/usr/bin/env python3
import random
from pyant import Canvas, Pixel
from pyant import Keys

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# Making sure there is enough place for the canvas
try:
    c = Canvas(32, 16)
except Exception as e:
    print(e)
    Canvas.quit()
c.fps = 4

# Initial snake state
snake = [[1, 1], [1, 2], [1, 3]]
treat = [0, 0]
score = -1


def retreat():
    '''
    A Function to be called anytime we create the treat
    '''
    global treat
    global score
    score += 1
    treat[0] = random.randint(0, c.width / 2 - 1)
    treat[1] = random.randint(0, c.height - 1)


retreat()
moving_direction = RIGHT
lock_changes = False


def locker(func):
    '''
    A wrapper function to make sure the direction is only being changed when it needs to
    '''
    def inner(arg):
        global lock_changes
        if not lock_changes:
            lock_changes = True
            func(arg)
            lock_changes = False
    return inner


# The following functions will be called every time the user changes the snake's direction
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


# Setting up the listeners
# Using both the arrow keys and WASD
c.on_click('a', move_left)
c.on_click(Keys.LEFT_KEY, move_left)
c.on_click('s', move_down)
c.on_click(Keys.DOWN_KEY, move_down)
c.on_click('w', move_up)
c.on_click(Keys.UP_KEY, move_up)
c.on_click('d', move_right)
c.on_click(Keys.RIGHT_KEY, move_right)


while not c._done:
    # Recoloring the background every frame
    c.set_all_pixels(Pixel(' ', Pixel.empty_color(), Pixel.hex_to_xterm_color(0x40ff60)))
    head = snake[-1]

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

    # Every part of the snake follows the next
    for i in range(len(snake) - 1):
        snake[i][0], snake[i][1] = snake[i + 1]
        if new_head_x == snake[i][0] and new_head_y == snake[i][1]:
            print('GG loser')
            Canvas.quit()
    snake[-2] = [head_x, head_y]
    snake[-1] = [new_head_x, new_head_y]

    # If snake is out of bounds
    if new_head_x < 0 or new_head_x * 2 >= c.width or new_head_y < 0 or new_head_y >= c.height:
        print('GG loser')
        Canvas.quit()

    # Putting the snake's pixels on the canvas
    for [x, y] in snake[:-1]:
        c.set_pixel(x, y, Pixel(' ', Pixel.empty_color(), Pixel.hex_to_xterm_color(0xf5e642)), square_mode=True)
    # A special treatment for the head
    c.set_pixel(new_head_x, new_head_y, Pixel('^', Pixel.empty_color(), Pixel.hex_to_xterm_color(0xffae21)), square_mode=True)

    # If the head of the snake is on the treat
    if new_head_x == treat[0] and new_head_y == treat[1]:
        # Add the treat to the snake
        snake.append([treat[0], treat[1]])
        retreat()
    else:
        # Show the treat if it wasn't eaten
        c.set_pixel(treat[0], treat[1], Pixel(' ', Pixel.empty_color(), Pixel.hex_to_xterm_color(0xff0000)), square_mode=True)
    lock_changes = False

    # Showing the score at the center
    title = f'score: {score}'
    c.text(title, int((c.width - len(title)) / 2), 0, foreground=Pixel.hex_to_xterm_color(0x000000))
    c.draw()
