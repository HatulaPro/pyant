import sys

if sys.platform != "linux" and sys.platform != "linux2":
    print('pyant only supports linux devices. Exiting.')
    exit(1)

from .canvas import Canvas, TERMINAL_DIMENSIONS
from .pixel import Pixel
from .input import Keys
