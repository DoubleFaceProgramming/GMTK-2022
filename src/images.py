import pygame

from src.globals import HEIGHT, TILE_SIZE, VEC

pygame.init()
pygame.display.set_mode()

def load_dice_img(num):
    return pygame.transform.smoothscale(pygame.image.load(f"res/assets/dice-{num}.png").convert(), (TILE_SIZE, TILE_SIZE))

dice_imgs = [
    load_dice_img(0),
    load_dice_img(1),
    load_dice_img(2),
    load_dice_img(3),
    load_dice_img(4),
    load_dice_img(5),
    load_dice_img(6)
]

amogus = pygame.transform.scale(pygame.image.load(f"res/assets/sussy.jpg").convert(), (TILE_SIZE, TILE_SIZE))
title_img = pygame.image.load("res/assets/title.png").convert_alpha()
title_img = pygame.transform.smoothscale(title_img, VEC(title_img.get_size()) * 0.6)

pygame.display.quit()