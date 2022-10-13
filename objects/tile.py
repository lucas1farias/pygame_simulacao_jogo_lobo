

import pygame
from random import choice
# from inks import colors


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, group, custom, w, h, image_path,):
        super().__init__(group)

        "QUANDO TILES SÃO RETÂNGULOS"
        # self.image = pygame.Surface((tile_size, tile_size))
        # self.image.fill(choice(colors))

        self.custom = custom
        if self.custom:
            "QUANDO TILES SÃO IMAGENS"
            self.w = w
            self.h = h
            self.image_path = image_path
            self.image = pygame.transform.scale(pygame.image.load(self.image_path), (self.w, self.h)).convert_alpha()
        else:
            "QUANDO TILES SÃO IMAGENS E ALEATÓRIAS"
            self.tile_sizes = [*range(25, 50)]
            self.image_types = [f'sprites/platforms/plat_{number}.gif' for number in range(1, 7)]

            "QUANDO SE QUER UM ITEM ALEATÓRIO"
            self.image = pygame.transform.scale(
                pygame.image.load(
                    choice(self.image_types)), (choice(self.tile_sizes), choice(self.tile_sizes))
            ).convert_alpha()

        # "pos" definido em: "Level/setup_level"
        self.rect = self.image.get_rect(center=pos)
