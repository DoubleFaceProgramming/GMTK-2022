from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING: from src.game import Game

from src.utils import rotate_dice, sign, newvec
from src.sprite import Sprite, LayersEnum
from src.images import dice_imgs, amogus
from build.exe_comp import pathof
from src.player import Player
from src.globals import *

from pygame.locals import *
from abc import abstractmethod
from json import loads
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
    def __init__(self, layer: int | LayersEnum, game: Game, pos: VEC):
        super().__init__(layer, game, pos)
        self.image.fill((200, 200, 200))

class DiceFace(Sprite):
    def __init__(self, game: Game, pos: VEC):
        super().__init__(LayersEnum.WORLD, game, pos)
        self.image.fill((255, 255, 255))

class Dice(Sprite):
    def __init__(self, layer: int | LayersEnum, game: Game, pos: VEC):
        super().__init__(LayersEnum.MOVEABLES, game, pos)
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
        if time.time() - self.roll_timer > 0.2:
            self.faces = rotate_dice(self.faces, direction)
            self.image = dice_imgs[self.faces[DIREC.TOP]["num"]]
            self.image = pygame.transform.rotate(self.image, self.faces[DIREC.TOP]["rot"])
            self.roll_timer = time.time()

    def update(self) -> None:
        player = self.game.level.player
        d_pos = player.pos - player.prev_pos # delta_pos

        base_pos = newvec(self.pos)
        r = self.image.get_rect()
        r.topleft = self.pos * TILE_SIZE - self.game.level.player.camera.offset

        screen_pos = self.pos * TILE_SIZE

        direction = None
        if player.rect.colliderect(r):
            if player.pos.y + player.size.y > screen_pos.y + TILE_SIZE + player.size.y - 3 and sign(d_pos.y) < 0:
                direction = DIREC.UP
                self.pos.y += sign(d_pos.y)
            elif player.pos.y < screen_pos.y - player.size.y + 3 and sign(d_pos.y) > 0:
                direction = DIREC.DOWN
                self.pos.y += sign(d_pos.y)
            elif player.pos.x + player.size.x > screen_pos.x + TILE_SIZE + player.size.x - 3 and sign(d_pos.x) < 0:
                direction = DIREC.LEFT
                self.pos.x += sign(d_pos.x)
            elif player.pos.x < screen_pos.x - player.size.x + 3 and sign(d_pos.x) > 0:
                direction = DIREC.RIGHT
                self.pos.x += sign(d_pos.x)

            if isinstance(self.game.level[self.pos], Void):
                player.pos = player.prev_pos # TODO: ex. dice on left, hold a, tapping s/w does nothing
                self.pos = base_pos
                num = self.faces[DIREC.TOP]["num"]

                positions = [self.pos + direction.value * i for i in range(1, num + 1)]
                level = self.game.level

                for pos in positions:
                    level[pos].kill()
                    level[pos] = DiceFace(self.game, pos)

                direction = None
                self.kill()
                level[self.pos] = None

            if direction:
                self.roll(direction)

    def draw(self):
        super().draw()
        r = self.image.get_rect()
        r.topleft = self.pos * TILE_SIZE - self.game.level.player.camera.offset

        pygame.draw.rect(self.game.screen, (255, 0, 0), r, width=2)

class End(Sprite):
    def __init__(self, layer: int | LayersEnum, game: Game, pos: VEC):
        super().__init__(layer, game, pos)
        self.image.blit(amogus, (0, 0))

class SpriteTypes(Enum):
    VOID = Void
    FLOOR = Floor
    PLAYER = Player
    DICE = Dice
    END = End

class Level:
    def __init__(self, game: Game, level_name: str):
        self.game = game

        path = pathof(f"res/levels/{level_name}.json")
        parsed = loads(open(path, "rb").read())
        legend = parsed["legend"]
        dice_data = parsed["die"]
        map_data = parsed["map"]

        self.map = []
        for i, row in enumerate(map_data):
            self.map.append([])
            for j, tile in enumerate(row):
                key = legend[str(tile)].upper()
                type_class = SpriteTypes[key].value
                if type_class != Player:
                    sprite = type_class(LayersEnum.WORLD, self.game, (j, i))
                    self.game.sprite_manager.add(sprite)
                    self.map[i].append(sprite)
                else:
                    player_tile_pos = (j, i)

        self.player = Player(LayersEnum.MOVEABLES, self.game, player_tile_pos)

    def __getitem__(self, key: VEC):
        return self.map[int(key.y)][int(key.x)]

    def __setitem__(self, key: VEC, value: ...):
        self.map[int(key.y) - 1][int(key.x) - 1] = value