from pygame.locals import *
from random import *
import pygame
import time
import sys

from src.sprite import SpriteManager
from src.player import Player
from src.level import Level
from src.globals import *


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | HWSURFACE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = self.clock.tick_busy_loop(FPS) / 1000

        pygame.display.set_caption("Just DIE!!")

        self.sprite_manager = SpriteManager()
        self.level = Level(self, "development")

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
        pygame.display.set_caption(f"Just DIE!! | {int(self.clock.get_fps())}")

        self.sprite_manager.update()

    def draw(self) -> None:
        self.screen.fill((20, 24, 28))

        self.sprite_manager.draw()
        pygame.display.flip()

    def quit(self) -> None:
        pygame.quit()
        sys.exit()