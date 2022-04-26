import random
from pyant import Canvas, Pixel

c = Canvas(40, 10)
c.clear_on_finish = False

for i in range(c.width * c.height):
    x = random.randint(0, c.width - 1)
    y = random.randint(0, c.height - 1)
    while c.get_pixel(x, y).character == 'X':
        x = random.randint(0, c.width - 1)
        y = random.randint(0, c.height - 1)

    c.get_pixel(x, y).character = 'X'
    if random.randint(0, 50) == 25:
        c.background(random.choice([Pixel.hex_to_xterm_color(0x00ff00), Pixel.hex_to_xterm_color(0xff0000), Pixel.hex_to_xterm_color(0x0000ff)]))
    c.draw()
