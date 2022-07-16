from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.player import Player
    from src.game import Game

from abc import abstractmethod
import pygame

from src.globals import VEC, TILE_SIZE

class Sprite:
    def __init__(self, game: Game, pos: VEC):
        self.game = game
        self.pos = VEC(pos)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos * TILE_SIZE
    
    def update(self):
        # Nothing in this but has to exist bcs update will be called on all tiles no matter what
        pass

    def draw(self):
        self.game.screen.blit(self.image, self.pos * TILE_SIZE - self.game.level.player.camera.offset)