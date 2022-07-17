from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING: from src.game import Game

from pygame.locals import K_SPACE, K_ESCAPE
import pygame

from src.sprite import SpriteManager
from src.images import title_img
from src.button import Button
from src.level import Level
from src.globals import *
from os import listdir

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
    def setup(self, path="map_1") -> None:
        super().setup()

        self.level = Level(self.game, path)

    def update(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            self.game.new_scene(self.game.Scenes.MainMenu)

        super().update()

    def draw(self) -> None:
        self.game.screen.fill((20, 24, 28))

        super().draw()

class MainMenu(Scene):
    def setup(self) -> None:
        super().setup()

        Button(self.game, (WIDTH // 2, 300), "Start Game", lambda: self.game.new_scene(self.game.Scenes.LevelsMenu))
        Button(self.game, (WIDTH // 2, 400), "Quit Game", self.game.quit)

    def update(self) -> None:
        keys = pygame.key.get_pressed()

        super().update()

    def draw(self) -> None:
        self.game.screen.fill((20, 24, 28))

        self.game.screen.blit(title_img, (WIDTH // 2 - title_img.get_width() // 2, 20))

        super().draw()

class LevelsMenu(Scene):
    def setup(self) -> None:
        super().setup()

        self.maps = {" ".join(map.removesuffix(".json").split("_")).capitalize(): map.removesuffix(".json") for map in listdir("res/levels")}

        for i, map in enumerate(self.maps.values()):
            Button(self.game, (WIDTH // 2, 50 + i * 50), "The one and only level", lambda map=map: self.game.new_scene(self.game.Scenes.MainGame, path=map), bloat=75)

    def draw(self):
        self.game.screen.fill((20, 24, 28))

        super().draw()