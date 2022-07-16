import pygame

from src.globals import TILE_SIZE

pygame.init()
pygame.display.set_mode()

def load_dice_img(num):
    return pygame.transform.scale(pygame.image.load(f"res/assets/dice-{num}.png").convert(), (TILE_SIZE, TILE_SIZE))

dice_imgs = [
    None, # Cuz the numbers start at 1
    load_dice_img(1),
    load_dice_img(2),
    load_dice_img(3),
    load_dice_img(4),
    load_dice_img(5),
    load_dice_img(6)
]

amogus = pygame.transform.scale(pygame.image.load(f"res/assets/sussy.jpg").convert(), (TILE_SIZE, TILE_SIZE))

pygame.display.quit()