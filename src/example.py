import random
from pyant import Canvas

c = Canvas(20, 10)

for i in range(200):
    x = random.randint(0, c.width - 1)
    y = random.randint(0, c.height - 1)
    while c.get_pixel(x, y) == ' ':
        x = random.randint(0, c.width - 1)
        y = random.randint(0, c.height - 1)
    c.set_pixel(' ', x, y)
    c.draw()

c.draw()
