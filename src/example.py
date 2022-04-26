import random
from pyant import Canvas

c = Canvas(40, 10)

for i in range(c.width * c.height):
    x = random.randint(0, c.width - 1)
    y = random.randint(0, c.height - 1)
    while c.get_pixel(x, y).character == 'X':
        x = random.randint(0, c.width - 1)
        y = random.randint(0, c.height - 1)

    c.get_pixel(x, y).character = 'X'
    c.draw()
