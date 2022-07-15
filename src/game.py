from pygame.locals import *
from random import *
import pygame
import time
import sys

from src.globals import *
from src.player import Player

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | HWSURFACE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = self.clock.tick_busy_loop(FPS) / 1000

        pygame.display.set_caption("Just DIE!!")

        self.player = Player(self)

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
        self.dt = self.clock.tick_busy_loop(FPS) / 1000
        self.events()

        self.player.update()

    def draw(self) -> None:
        self.screen.fill((20, 24, 28))

        self.player.draw()

        pygame.display.flip()

    def quit(self) -> None:
        pygame.quit()
        sys.exit()