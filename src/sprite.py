from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.player import Player
    from src.game import Game

from src.globals import VEC, TILE_SIZE
from abc import abstractmethod
from enum import Enum, auto
from pygame import Surface
from typing import Any
import pygame

# This code was taken from 2DMC (not copyrighted because the developers and creators are USSSSSS)
# https://github.com/DoubleFaceProgramming/2DMC/blob/master/src/sprite.py <--- go check us out (pls)

class LayersEnum(Enum):
    WORLD = auto()
    MOVEABLES = auto()
    VOID = auto()

class Sprite:
    """A common baseclass for all sprites."""

    def __init__(self, layer: int | LayersEnum, game: Game, pos: VEC) -> None:
        # Setting the layer attribute. This defines where in the draw order the sprite will be drawn.
        # See SpriteHandler.draw()
        # In theory try except is faster as layer will almost always be an enum, so may as well
        try:
            self._layer = layer.value
        except AttributeError:
            if isinstance(layer, int):
                self._layer = layer
            else:
                raise TypeError("Argument 'layer' must be of type 'int' or 'Enum item'")

        self.game = game
        self.scene = self.game.scene
        self.pos = VEC(pos)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos * TILE_SIZE
        self.scene.sprite_manager.add(self)

    def update(self) -> None:
        """Update the classes attributes and variables or handle class logic related to the class.
        Args:
            dt (float): Delta time
            **kwargs (dict[Any]): Class specific arguments
        """

    def draw(self) -> None:
        """Draw the sprite to the screen
        Args:
            screen (Surface): The screen to draw to
            **kwargs (dict[Any]): Class specific arguments
        """
        self.game.screen.blit(self.image, self.pos * TILE_SIZE - self.scene.level.player.camera.offset)

    def kill(self) -> None:
        """Kill the sprite and handle any cleanup logic"""
        try:
            self.scene.sprite_manager.remove(self)
        except SpriteNotFoundException:
            print("LIFE IS SUFFERING")
        del self

class NoLayerAttributeException(Exception):
    """If the sprite does not have a layer attribute"""

    def __init__(self, sprite: Sprite) -> None:
        self.sprite = sprite

    def __str__(self) -> str:
        return f"Class {self.sprite.__class__} does not have a _layer / _debug_layer attribute!"

class LayerNotFoundException(Exception):
    """If the sprites layer did not exist in the layer dict"""

    def __init__(self, arg: int | Sprite) -> None:
        if isinstance(arg, Sprite):
            arg = arg._layer
        self._layer = arg

    def __str__(self) -> str:
        return f"Layer {LayersEnum(self._layer).name} does not exist in the layer list!"

class SpriteNotFoundException(Exception):
    """If the sprite did not exist inside the layer"""

    def __init__(self, sprite: Sprite) -> None:
        self.sprite = sprite

    def __str__(self) -> str:
        return f"Sprite object {self.sprite} does not exist in the sprite list!"

class SpriteManager:
    """A class to simplify and better how sprites are drawn and managed"""

    def __init__(self, *args: tuple[Sprite]) -> None:
        self.layers = {}
        if args: # You can create a spritehandler without specifying any args
            self.add(*args)

    def __iter__(self) -> SpriteManager:
        # Sorting the layer dict so that the lowest layer (layer that should be drawn first)
        # is first, and the highest is drawn last
        self.layers = dict(sorted(self.layers.items()))
        self.layeriter = self.spriteiter = 0
        self.get_layer = lambda: list(self.layers.values())[self.layeriter-1]
        return self

    # Bad code but i just cba at this point this has taken way too long
    def __next__(self) -> Sprite:
        # If the current layer is greater than the number of layers, stop the iteration (this exits a for loop)
        if self.layeriter >= len(self.layers):
            raise StopIteration

        # The layers dict is keyed by the layer, but we need it to be keyed by its index
        # Ideally this would be in __iter__ but fsr it crashes so.. ¯\_(ツ)_/¯
        layer = self.get_layer()
        self.spriteiter += 1
        if self.spriteiter >= len(layer): # Then check if it is greater than it's max.
            self.spriteiter = 0

            # We dont want to return sprites in debug layers, as they would be returned in their respective normal layers so would just cause repetition.
            # If the next layer is a debug layer, keep on incrementing the layer counter until it is no longer a debug layer
            # This could benefit from a do / while loop :o (python please add it its actually useful)
            while True:
                self.layeriter += 1
                if not LayersEnum(list(self.layers)[self.layeriter - 1]).name.endswith("_DEBUG"):
                    layer = self.get_layer() # Recalculating layer with the new layer iteration attribute
                    break

        return layer[self.spriteiter]

    def __contains__(self, sprite: Sprite) -> bool:
        try:
            return sprite in self.layers[sprite._layer]
        except AttributeError: # No layer attribute
            raise NoLayerAttributeException(sprite)
        except KeyError: # Layer not found
            # We dont want it to throw an error, but may as well have a warning
            print(str(LayerNotFoundException(sprite)))
            return False

    def add(self, *args: tuple[Sprite]) -> None:
        """Add any number of sprites to the list of sprites
        Args:
            *args (tuple of Sprites): The sprites to add (can be of arbitary length)
        Raises:
            NoLayerAttributeException: If any given sprite does not have a layer attribute
        """

        for sprite in args:
            try:
                if sprite._layer not in self.layers: # Make a new layer
                    self.layers[sprite._layer] = [sprite]
                else: # Add the sprite to a pre-existing layer
                    self.layers[sprite._layer].append(sprite)
            # Try / Except is faster
            # Raised if the sprite does not have a layer / debug layer attribute
            except AttributeError:
                raise NoLayerAttributeException(sprite)

    def remove(self, sprite: Sprite) -> None:
        try: # Remove the sprite
            self.layers[sprite._layer].remove(sprite)
        except ValueError: # If the sprite was not in its corresponding layer list
            raise SpriteNotFoundException(sprite)
        except KeyError: # If the sprite's layer was not in the layer dict
            raise LayerNotFoundException(sprite._layer)

        # If the layer list is empty, delete it
        # (Having an empty list breaks iteration)
        if not self.layers[sprite._layer]:
            del self.layers[sprite._layer]

    def draw(self) -> None:
        # We need to copy self.layers because otheriwse when sprites are created whilst rendering it would crash
        for layer in (layers := self.layers.copy()): # Loop through every layer
            for sprite in layers[layer]: # Loop through every sprite
                sprite.draw()

    def update(self) -> None:
        for sprite in self:
            sprite.update()