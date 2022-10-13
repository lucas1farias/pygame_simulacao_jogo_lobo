

import pygame
from objects.scenario import Level

pygame.init()
screen_w, screen_h = 1200, 600
screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()

level = Level()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        # Única maneira achada de mudar os sprites p/ "parado"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                level.player.idle_right_setup()
            if event.key == pygame.K_a:
                level.player.idle_left_setup()

    "ANTES DE TER IMAGENS DE FUNDO (corrige borrão de imagens, p/ ver borrão, desative)"
    screen.fill('#222222')

    level.run()
    level.printer()

    pygame.display.update()
    clock.tick(30)
