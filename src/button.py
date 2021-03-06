from __future__ import annotations
from tkinter import CENTER
from typing import TYPE_CHECKING

if TYPE_CHECKING: from src.game import Game

from src.sprite import Sprite, LayersEnum
from src.globals import *

from pygame.locals import MOUSEBUTTONUP
from typing import Callable
import pygame

class Button(Sprite):
    def __init__(self, game: Game, pos: VEC, text: str | pygame.Surface, func: Callable, anchor: Anchor = Anchor.CENTER, bloat: int = 120) -> None:
        super().__init__(LayersEnum.GUI, game, pos)
        self.func = func
        if type(text) == pygame.Surface:
            self.image = text
            self.text = ""
        else:
            self.image = pygame.Surface((0, 0))
            self.text = str(text)
        self.text_color = (199, 199, 199)
        self.bg_color = (141, 144, 215)
        self.border_color = (80, 85, 234)
        self.text_surf = FONT.render(self.text, True, self.text_color)
        self.bloat = bloat
        if self.text:
            self.text_size = VEC(self.text_surf.get_size())
        else:
            self.text_size = VEC(self.image.get_size())
        self.size = self.text_size * (1 + self.bloat / 100)
        self.size_diff = (self.size - self.text_size) // 2
        if anchor == Anchor.CENTER:
            self.pos = VEC(pos) - VEC(anchor.value.x * self.size_diff.x, anchor.value.y * self.size.y) / 2
            self.pos = self.pos - VEC((anchor.value.x + 1) * self.size.x, (anchor.value.y + 1) * self.size.y) // 2
        elif anchor == Anchor.TOPLEFT:
            self.pos = VEC(pos)
        self.text_pos = self.pos + (self.size - self.text_size) // 2
        self.rect = pygame.Rect(self.pos, self.size)

    def update(self) -> None:
        m_pos = VEC(pygame.mouse.get_pos())
        for event in self.game.events:
            if event.type == MOUSEBUTTONUP:
                if self.rect.collidepoint(m_pos):
                    self.func()

    def draw(self) -> None:
        pygame.draw.rect(self.game.screen, self.bg_color, (*self.pos, *self.size))
        pygame.draw.rect(self.game.screen, self.border_color, (*self.pos, *self.size), 4)
        self.game.screen.blit(self.text_surf if self.text else self.image, self.text_pos)