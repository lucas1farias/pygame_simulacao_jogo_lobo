

import pygame


class Landscape(pygame.sprite.Sprite):
    def draw(self):
        self.canvas.blit(self.image, (self.x, self.y))

    def __init__(self, image_path, x, y, group):
        super().__init__(group)
        self.x = x
        self.y = y
        self.canvas = pygame.display.get_surface()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image_width = self.image.get_width()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.vector = None
