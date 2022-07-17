from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING: from src.game import Game

from pygame.locals import K_SPACE, K_ESCAPE, SRCALPHA
import pygame

from src.images import title_img, restart_img, smol_dice_imgs, home_img
from src.sprite import SpriteManager
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

        self.level_path = path
        self.level = Level(self.game, self.level_path)
        Button(self.game, (10, 10), home_img, lambda: self.game.new_scene(self.game.Scenes.MainMenu), anchor=Anchor.TOPLEFT, bloat=30)
        Button(self.game, (10, 80), restart_img, lambda: self.game.new_scene(self.game.Scenes.MainGame, path=self.level_path), anchor=Anchor.TOPLEFT, bloat=30)

    def update(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            self.game.new_scene(self.game.Scenes.MainMenu)

        super().update()

    def draw(self) -> None:
        self.game.screen.fill((20, 24, 28))

        self.sprite_manager.draw()

        faces = self.level.dice.faces
        screen = self.game.screen

        img = lambda direc: smol_dice_imgs[faces[direc]["num"]]

        sw = screen.get_width() # screen width
        ie = img(Direc.TOP).get_width() # image edge (size)
        m = 10 # margin
        c = ie # correction

        transparent_surf = pygame.Surface((ie * 4, ie * 4), SRCALPHA)
        transparent_surf.fill((255, 255, 255, 80))
        screen.blit(transparent_surf, (sw - ie * 4 - m, 1 * ie + m - c))

        screen.blit(img(Direc.BOTTOM), (sw - ie * 2 - m - ie / 2, 2 * ie + m - c + ie / 2))
        screen.blit(img(Direc.LEFT),   (sw - ie * 3 - m - ie / 2, 2 * ie + m - c + ie / 2))
        screen.blit(img(Direc.RIGHT),  (sw - ie * 1 - m - ie / 2, 2 * ie + m - c + ie / 2))
        screen.blit(img(Direc.DOWN),   (sw - ie * 2 - m - ie / 2, 3 * ie + m - c + ie / 2))
        screen.blit(img(Direc.UP),     (sw - ie * 2 - m - ie / 2, 1 * ie + m - c + ie / 2))

        pygame.display.flip()

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

        for i, map in enumerate(self.maps.items()):
            Button(self.game, (WIDTH // 2, 50 + i * 75), map[0], lambda map=map: self.game.new_scene(self.game.Scenes.MainGame, path=map[1]), bloat=75)

    def draw(self):
        self.game.screen.fill((20, 24, 28))

        super().draw()