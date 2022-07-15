from pygame.math import Vector2 as VEC
from enum import Enum

FPS = 256
WIDTH = 800
HEIGHT = 800
TILE_SIZE = 80

class DIREC(Enum):
    UP = VEC(0, -1)
    DOWN = VEC(0, 1)
    LEFT = VEC(-1, 0)
    RIGHT = VEC(1, 0)