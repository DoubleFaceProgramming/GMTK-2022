from pygame.locals import *
from random import * # TODO: "*"" bad :(
import pygame
import time
import sys

from src.globals import *

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | HWSURFACE)
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            self.update()
            self.draw()

        self.quit()

    def events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

    def update(self) -> None:
        self.clock.tick_busy_loop(144)
        self.events()

    def draw(self) -> None:
        pygame.display.flip()

    def quit(self) -> None:
        pygame.quit()
        sys.exit()