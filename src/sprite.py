from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING: from src.game import Game

from abc import abstractmethod

class Sprite:
    def __init__(self, game: Game) -> None:
        self.game = game

    @abstractmethod
    def update(self) -> None:
        pass
    
    @abstractmethod
    def draw(self) -> None:
        pass