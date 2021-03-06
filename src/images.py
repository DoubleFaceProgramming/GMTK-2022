import pygame

from src.globals import HEIGHT, TILE_SIZE, VEC
from build.exe_comp import pathof

pygame.init()
pygame.display.set_mode()

def load_tile(path, scalefunc=pygame.transform.smoothscale):
    return scalefunc(pygame.image.load(pathof(path)).convert_alpha(), (TILE_SIZE, TILE_SIZE))

dice_imgs = [load_tile(f"res/assets/dice-{num}.png") for num in range(6 + 1)]
smol_dice_imgs = [pygame.transform.smoothscale(img, VEC(img.get_size()) * 0.5) for img in dice_imgs]
dice_tile_imgs = [None] + [load_tile(f"res/assets/dice_tile-{num}.png", pygame.transform.scale) for num in range(1, 6 + 1)]
floor_imgs = [load_tile(f"res/assets/floor-{num}.png", pygame.transform.scale) for num in range(3)]
wall_img = load_tile("res/assets/wall.png", pygame.transform.scale).convert()
dark_wall_img = load_tile("res/assets/wall_dark.png", pygame.transform.scale).convert()
void_img = [None] + [load_tile(f"res/assets/void-{num}.png", pygame.transform.scale).convert() for num in range(1, 3 + 1)]
end = load_tile("res/assets/end.png")
title_img = pygame.image.load(pathof("res/assets/title.png")).convert_alpha()
title_img = pygame.transform.smoothscale(title_img, VEC(title_img.get_size()) * 0.6)
restart_img = pygame.image.load(pathof("res/assets/restart.png")).convert_alpha()
restart_img = pygame.transform.smoothscale(restart_img, VEC(restart_img.get_size()) * 0.1)
home_img = pygame.image.load(pathof("res/assets/home.png")).convert_alpha()
home_img = pygame.transform.smoothscale(home_img, restart_img.get_size())
player_img = pygame.image.load(pathof("res/assets/player.png")).convert_alpha()
player_img = pygame.transform.smoothscale(player_img, (TILE_SIZE / 1.5, TILE_SIZE / 1.5))

pygame.display.quit()