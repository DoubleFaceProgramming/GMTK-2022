from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING: from src.game import Game

from pygame.locals import K_SPACE, K_ESCAPE
import pygame

from src.sprite import SpriteManager
from src.images import title_img
from src.level import Level
from src.globals import *

class Scene:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.running = True

    def setup(self) -> None:
        self.sprite_manager = SpriteManager()

    def update(self) -> None:
        self.sprite_manager.update()

    def draw(self) -> None:
        self.sprite_manager.draw()
        pygame.display.flip()

class MainGame(Scene):
    def setup(self) -> None:
        super().setup()

        self.level = Level(self.game, "map_1")

    def update(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            self.game.new_scene(self.game.Scenes.MainMenu)

        super().update()

    def draw(self) -> None:
        self.game.screen.fill((20, 24, 28))

        super().draw()

class MainMenu(Scene):
    def update(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            self.game.new_scene(self.game.Scenes.MainGame)

        super().update()

    def draw(self) -> None:
        self.game.screen.fill((20, 24, 28))

        self.game.screen.blit(title_img, (WIDTH // 2 - title_img.get_width() // 2, 20))

        super().draw()