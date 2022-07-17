import pygame

from src.globals import HEIGHT, TILE_SIZE, VEC

pygame.init()
pygame.display.set_mode()

def load_tile(path, scalefunc=pygame.transform.smoothscale):
    return scalefunc(pygame.image.load(path).convert_alpha(), (TILE_SIZE, TILE_SIZE))

dice_imgs = [load_tile(f"res/assets/dice-{num}.png") for num in range(6 + 1)]
dice_tile_imgs = [None] + [load_tile(f"res/assets/dice_tile-{num}.png", pygame.transform.scale) for num in range(1, 6 + 1)]
floor_imgs = [load_tile(f"res/assets/floor-{num}.png", pygame.transform.scale) for num in range(3)]
wall_img = load_tile("res/assets/wall.png", pygame.transform.scale).convert()
dark_wall_img = load_tile("res/assets/wall_dark.png", pygame.transform.scale).convert()
void_img = [None] + [load_tile(f"res/assets/void-{num}.png", pygame.transform.scale).convert() for num in range(1, 3 + 1)]
amogus = load_tile("res/assets/sussy.jpg")
title_img = pygame.image.load("res/assets/title.png").convert_alpha()
title_img = pygame.transform.smoothscale(title_img, VEC(title_img.get_size()) * 0.6)

pygame.display.quit()