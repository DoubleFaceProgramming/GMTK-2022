from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING: from src.game import Game

import pygame

from src.sprite import SpriteManager
from src.level import Level

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
    def __init__(self, game: Game) -> None:
        super().__init__(game)

    def setup(self) -> None:
        super().setup()
        self.level = Level(self.game, "map_1")

    def draw(self) -> None:
        self.game.screen.fill((20, 24, 28))
        
        super().draw()