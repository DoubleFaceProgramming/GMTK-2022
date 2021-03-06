from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING: from src.game import Game

from src.sprite import Sprite, LayersEnum
from src.utils import rotate_dice, sign
from build.exe_comp import pathof
from src.player import Player
from src.globals import *
from src.images import *

from random import choices, randint
from abc import abstractmethod
from pygame.locals import *
from json import loads
from enum import Enum
import pygame
import time

class Void(Sprite):
    def __init__(self, layer, game: Game, pos: VEC) -> None:
        super().__init__(LayersEnum.VOID, game, pos)
        self.image = pygame.transform.rotate(void_img[randint(1, 3)], randint(0, 3) * 90)

    def update(self) -> None:
        player = self.scene.level.player

        r = self.image.get_rect()
        r.topleft = self.pos * TILE_SIZE - player.camera.offset

        if player.rect.colliderect(r):
            player.pos = player.prev_pos

class Floor(Sprite):
    def __init__(self, layer: int | LayersEnum, game: Game, pos: VEC):
        super().__init__(layer, game, pos)
        self.image = floor_imgs[choices([0, 1, 2], [12, 1, 1])[0]]

class DiceFace(Sprite):
    def __init__(self, game: Game, pos: VEC, top):
        super().__init__(LayersEnum.WORLD, game, pos)
        self.image = dice_tile_imgs[top["num"]]

class Dice(Sprite):
    def __init__(self, layer: int | LayersEnum, game: Game, pos: VEC):
        super().__init__(LayersEnum.MOVEABLES, game, pos)
        self.faces = {
            Direc.TOP: {"num": 1, "rot": 0},
            Direc.BOTTOM: {"num": 4, "rot": 0},
            Direc.UP: {"num": 2, "rot": 0},
            Direc.DOWN: {"num": 5, "rot": 0},
            Direc.LEFT: {"num": 6, "rot": 0},
            Direc.RIGHT: {"num": 3, "rot": 0}
        }
        self.image = dice_imgs[self.faces[Direc.TOP]["num"]]
        self.create_tile_timer = time.time()
        self.tile_positions = []

    def roll(self, direction: Direc) -> None:
        self.faces = rotate_dice(self.faces, direction)
        self.image = dice_imgs[self.faces[Direc.TOP]["num"]]
        self.image = pygame.transform.rotate(self.image, self.faces[Direc.TOP]["rot"])

    def update(self) -> None:
        player = self.scene.level.player
        d_pos = player.pos - player.prev_pos # delta_pos

        base_pos = self.pos.copy()
        r = self.image.get_rect()
        r.topleft = self.pos * TILE_SIZE - self.scene.level.player.camera.offset

        screen_pos = self.pos * TILE_SIZE

        direction = None
        if player.rect.colliderect(r):
            if player.pos.y + player.size.y > screen_pos.y + TILE_SIZE + player.size.y - 3 and sign(d_pos.y) < 0:
                direction = Direc.UP
                self.pos.y += sign(d_pos.y)
            elif player.pos.y < screen_pos.y - player.size.y + 3 and sign(d_pos.y) > 0:
                direction = Direc.DOWN
                self.pos.y += sign(d_pos.y)
            elif player.pos.x + player.size.x > screen_pos.x + TILE_SIZE + player.size.x - 3 and sign(d_pos.x) < 0:
                direction = Direc.LEFT
                self.pos.x += sign(d_pos.x)
            elif player.pos.x < screen_pos.x - player.size.x + 3 and sign(d_pos.x) > 0:
                direction = Direc.RIGHT
                self.pos.x += sign(d_pos.x)

            if isinstance(self.scene.level[self.pos], Wall):
                player.pos = player.prev_pos.copy()
                self.pos = base_pos.copy()
                direction = None
            elif isinstance(self.scene.level[self.pos], Void):
                self.prev_top = self.faces[Direc.TOP].copy()
                player.pos = player.prev_pos.copy()
                self.pos = base_pos.copy()
                num = self.faces[Direc.TOP]["num"]

                self.faces[Direc.TOP]["num"] = 0
                self.tile_positions = [self.pos + direction.value * i for i in range(1, num + 1)]

                direction = None

            if direction:
                self.roll(direction)

        if self.tile_positions and time.time() - self.create_tile_timer > 0.1:
            self.create_tile_timer = time.time()
            pos = self.tile_positions[0]
            self.tile_positions.pop(0)
            try:
                if type(self.scene.level[pos]) == Void:
                    self.scene.level[pos].kill()
                    self.scene.level[pos] = DiceFace(self.game, pos, self.prev_top)
            except AttributeError:
                pass

    def draw(self):
        super().draw()
        r = self.image.get_rect()
        r.topleft = self.pos * TILE_SIZE - self.scene.level.player.camera.offset

class End(Sprite):
    def __init__(self, layer: int | LayersEnum, game: Game, pos: VEC):
        super().__init__(layer, game, pos)
        self.image.blit(end, (0, 0))

    def update(self) -> None:
        player = self.scene.level.player

        r = self.image.get_rect()
        r.topleft = self.pos * TILE_SIZE - player.camera.offset

        if player.rect.colliderect(r):
            self.game.new_scene(self.game.Scenes.LevelsMenu)

class Wall(Sprite):
    def __init__(self, layer: int | LayersEnum, game: Game, pos: VEC) -> None:
        super().__init__(layer, game, pos)
        self.image = wall_img

    def update(self) -> None:
        player = self.scene.level.player

        r = self.image.get_rect()
        r.topleft = self.pos * TILE_SIZE - player.camera.offset

        if player.rect.colliderect(r):
            player.pos = player.prev_pos

class DarkerWall(Wall):
    def __init__(self, layer: int | LayersEnum, game: Game, pos: VEC) -> None:
        super().__init__(layer, game, pos)
        self.image = dark_wall_img


class SpriteTypes(Enum):
    VOID = Void
    FLOOR = Floor
    PLAYER = Player
    DICE = Dice
    END = End
    WALL = Wall
    DARK_WALL = DarkerWall

class Level:
    def __init__(self, game: Game, level_name: str):
        self.game = game

        path = pathof(f"res/levels/{level_name}.json")
        parsed = loads(open(path, "rb").read())
        legend = parsed["legend"]
        map_data = parsed["map"]

        self.die = []
        self.map = []
        for i, row in enumerate(map_data):
            self.map.append([])
            for j, tile in enumerate(row):
                key = legend[tile].upper()
                type_class = SpriteTypes[key].value
                if type_class == Player:
                    player_tile_pos = (j, i)
                    sprite = Floor(LayersEnum.WORLD, self.game, (j, i))
                elif type_class == Dice:
                    dice_pos = (j, i)
                    sprite = Floor(LayersEnum.WORLD, self.game, (j, i))
                else:
                    sprite = type_class(LayersEnum.WORLD, self.game, (j, i))
                self.map[i].append(sprite)

        self.player = Player(LayersEnum.MOVEABLES, self.game, player_tile_pos)
        self.dice = Dice(LayersEnum.MOVEABLES, self.game, dice_pos)

    def __getitem__(self, key: VEC):
        try:
            return self.map[int(key.y)][int(key.x)]
        except:
            pass

    def __setitem__(self, key: VEC, value: ...):
        self.map[int(key.y)][int(key.x)] = value