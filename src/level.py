from build.exe_comp import pathof
from src.player import Player
from src.globals import *

from abc import abstractmethod
from enum import Enum
import pygame

class Object:
    def __init__(self, pos: VEC):
        self.pos = VEC(pos)
        # self.image = pygame.Surface(())

    def player_interacts(self, player: Player):
        return True

class Void(Object):
    def player_interacts(self, player: Player):
        return False

class Floor(Object): pass
class Dice(Object):
    # def __init__(self, pos: VEC):
        
    #     super().__init__(pos)
    
    def player_interacts(self, player: Player):
        return False


class ObjectTypes(Enum):
    VOID = Void
    FLOOR = Floor
    PLAYER = Player
    DICE = Dice

class Level:
    def __init__(self, level_name: str):
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
                self.map[i].append(ObjectTypes[legends[tile].upper()].value((i, j))) # 🤮

    def __gettitem__(self, key):
        pass