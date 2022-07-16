from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING: from src.game import Game

from build.exe_comp import pathof
from src.utils import rotate_dice
from src.images import dice_imgs
from src.sprite import Sprite
from src.player import Player
from src.globals import *

from pygame.locals import *
from abc import abstractmethod
from enum import Enum
import pygame
import time

class Void(Sprite):
    def update(self) -> None:
        player = self.game.level.player
        d_pos = player.pos - player.prev_pos # delta_pos
        new_rect = pygame.Rect(player.prev_pos.x + d_pos.x, player.prev_pos.y, *player.size) # player rect but we move x first
        if new_rect.colliderect(self.rect):
            pixel_pos = self.pos * TILE_SIZE # pixel position of this tile
            if d_pos.x > 0: # left collision pushout
                player.pos.x = pixel_pos.x - player.size.x
            elif d_pos.x < 0: # right collision pushout
                player.pos.x = pixel_pos.x + TILE_SIZE
        new_rect = pygame.Rect(player.pos.x, player.prev_pos.y + d_pos.y, *player.size) # we move y now
        if new_rect.colliderect(self.rect):
            pixel_pos = self.pos * TILE_SIZE # pixel position of this tile
            if d_pos.y > 0: # top collision pushout
                player.pos.y = pixel_pos.y - player.size.y
            elif d_pos.y < 0: # bottom collision pushout
                player.pos.y = pixel_pos.y + TILE_SIZE

class Floor(Sprite):
    def __init__(self, game: Game, pos: VEC):
        super().__init__(game, pos)
        self.image.fill((200, 200, 200))

class Dice(Sprite):
    def __init__(self, game: Game, pos: VEC):
        super().__init__(game, pos)
        # self.image.fill((0, 255, 0))
        self.faces = {
            DIREC.TOP: {"num": 1, "rot": 0},
            DIREC.BOTTOM: {"num": 4, "rot": 0},
            DIREC.UP: {"num": 2, "rot": 0},
            DIREC.DOWN: {"num": 5, "rot": 0},
            DIREC.LEFT: {"num": 6, "rot": 0},
            DIREC.RIGHT: {"num": 3, "rot": 0}
        }
        self.image = dice_imgs[self.faces[DIREC.TOP]["num"]]
        self.roll_timer = time.time()

    def roll(self, direction: DIREC) -> None:
        if time.time() - self.roll_timer > 1.5:
            self.faces = rotate_dice(self.faces, direction)
            self.image = dice_imgs[self.faces[DIREC.TOP]["num"]]
            self.image = pygame.transform.rotate(self.image, self.faces[DIREC.TOP]["rot"])
            self.roll_timer = time.time()

    def update(self) -> None:
        player = self.game.level.player
        d_pos = player.pos - player.prev_pos # delta_pos
        new_rect = pygame.Rect(player.prev_pos.x + d_pos.x, player.prev_pos.y, *player.size) # player rect but we move x first
        if new_rect.colliderect(self.rect):
            pixel_pos = self.pos * TILE_SIZE # pixel position of this tile
            if d_pos.x > 0: # left collision pushout
                player.pos.x = pixel_pos.x - player.size.x
                self.roll(DIREC.RIGHT) # player is left, roll right
            elif d_pos.x < 0: # right collision pushout
                player.pos.x = pixel_pos.x + TILE_SIZE
                self.roll(DIREC.LEFT) # player is right, roll left
        new_rect = pygame.Rect(player.pos.x, player.prev_pos.y + d_pos.y, *player.size) # we move y now
        if new_rect.colliderect(self.rect):
            pixel_pos = self.pos * TILE_SIZE # pixel position of this tile
            if d_pos.y > 0: # top collision pushout
                player.pos.y = pixel_pos.y - player.size.y
                self.roll(DIREC.DOWN) # player is up, roll down
            elif d_pos.y < 0: # bottom collision pushout
                player.pos.y = pixel_pos.y + TILE_SIZE
                self.roll(DIREC.UP) # player is down, roll up

class SpriteTypes(Enum):
    VOID = Void
    FLOOR = Floor
    PLAYER = Player
    DICE = Dice

class Level:
    def __init__(self, game: Game, level_name: str):
        self.game = game

        path = pathof(f"res/levels/{level_name}.jdmap")
        contents = [raw.strip() for raw in open(path).readlines() if raw != "\n"]

        for index, line in enumerate(contents):
            if line == "-":
                delimiter = int(index)
                break

        legends = {}
        for entry in contents[:delimiter]:
            key, value = [token.strip() for token in entry.split(":")]
            legends.update({key: value})

        data = []
        for row in contents[delimiter + 1:]:
            data.append([tile for tile in row])

        self.map = []
        for i, row in enumerate(data):
            self.map.append([])
            for j, tile in enumerate(row):
                key = legends[tile].upper()
                type_class = SpriteTypes[key].value
                if type_class != Player:
                    sprite = type_class(self.game, (j, i))
                    self.map[i].append(sprite)
                else:
                    player_tile_pos = (j, i)
        self.player = Player(self.game, player_tile_pos)

    def update(self):
        self.player.update()

        for row in self.map:
            for tile in row:
                tile.update()

    def draw(self):
        for row in self.map:
            for tile in row:
                tile.draw()

        self.player.draw()