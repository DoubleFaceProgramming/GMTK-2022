from pygame.locals import *
from random import *
import pygame
import time
import sys

from src.scene import MainGame
from src.player import Player
from src.globals import *

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | HWSURFACE)
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick_busy_loop(FPS) / 1000

        pygame.display.set_caption("Just DIE!!")

        self.scene = MainGame(self)
        self.scene.setup()

    def run(self):
        while self.scene.running:
            self.update()
            self.scene.update()
            self.scene.draw()

        self.quit()

    def events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()

    def update(self) -> None:
        self.dt = self.clock.tick_busy_loop(FPS) / 1000
        pygame.display.set_caption(f"Just DIE!! | {int(self.clock.get_fps())}")
        self.events()

    def new_scene(self, scene_class: str) -> None:
        self.scene.running = False
        self.scene = self.Scenes[scene_class].value(self, self.scene)
        self.scene.setup()

    def quit(self) -> None:
        pygame.quit()
        sys.exit()