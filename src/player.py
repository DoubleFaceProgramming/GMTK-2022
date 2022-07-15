from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING: from src.game import Game

from pygame.locals import *
import pygame

from src.globals import *
from src.utils import intvec
from src.sprite import Sprite

class Camera:
    def __init__(self, game: Game, player: Player) -> None:
        self.game = game
        self.player = player
        self.actual_offset = self.player.pos - VEC(WIDTH, HEIGHT) / 2
        self.offset = intvec(self.actual_offset)

    def update(self) -> None:
        tick_offset = self.player.pos - self.offset - VEC(WIDTH, HEIGHT) / 2
        if -1 < tick_offset.x < 1:
            tick_offset.x = 0
        if -1 < tick_offset.y < 1:
            tick_offset.y = 0
        self.actual_offset += tick_offset * 3 * self.game.dt
        self.offset = intvec(self.actual_offset)

class Player(Sprite):
    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.size = VEC(30, 30)
        self.pos = VEC(WIDTH // 2 - self.size.y // 2, HEIGHT // 2 - self.size.y // 2)
        self.vel = VEC(0, 0)
        self.direction = DIREC.UP
        self.camera = Camera(self.game, self)

    def update(self) -> None:
        self.camera.update()

        keys = pygame.key.get_pressed()
        self.vel = VEC(0, 0)
        if not (keys[K_w] and keys[K_s]):
            if keys[K_w]: self.vel.y = -100
            elif keys[K_s]: self.vel.y = 100
        if not (keys[K_a] and keys[K_d]):
            if keys[K_a]: self.vel.x = -100
            elif keys[K_d]: self.vel.x = 100

        self.pos += self.vel * self.game.dt

    def draw(self) -> None:
        pygame.draw.rect(self.game.screen, (255, 0, 0), (*(self.pos - self.camera.offset), *self.size), 2)