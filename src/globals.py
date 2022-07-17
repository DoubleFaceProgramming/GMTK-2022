from pygame.math import Vector2 as VEC
from enum import Enum
import pygame

FPS = 256
WIDTH = 810
HEIGHT = 500
TILE_SIZE = 80

class Direc(Enum):
    UP = VEC(0, -1)
    DOWN = VEC(0, 1)
    LEFT = VEC(-1, 0)
    RIGHT = VEC(1, 0)
    TOP = 1
    BOTTOM = -1

class Anchor(Enum):
    TOP = VEC(0, -1)
    BOTTOM = VEC(0, 1)
    LEFT = VEC(-1, 0)
    RIGHT = VEC(1, 0)
    CENTER = VEC(0, 0)
    TOPLEFT = VEC(-1, -1)
    TOPRIGHT = VEC(1, -1)
    BOTTOMLEFT = VEC(-1, 1)
    BOTTOMRIGHT = VEC(1, 1)

pygame.font.init()
FONT = pygame.font.Font("res/fonts/Dungeons-D6mE.ttf", 32)