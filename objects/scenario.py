

import pygame
from config.settings import *
from objects.tile import Tile
from objects.player import Player
from random import choice
from objects.enemy import Enemy


class Level:
    def __init__(self):
        self.canvas = pygame.display.get_surface()
        self.player = None
        "ANTES DA ANIMAÇÃO EXISTIR"
        # self.visible_sprites = pygame.sprite.Group()
        "DEPOIS"
        self.visible_sprites = Camera()
        self.active_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.setup_level(target_map=scenario4)
        self.terrain = None
        self.stone_block = None
        self.wooden_box = None
        self.shell = None

    def run(self):
        # Essa ordem deve ser respeitada
        self.active_sprites.update()

        "ANTES DA CÂMERA"
        # self.visible_sprites.draw(self.canvas)

        "DESENHO DOS SPRITES DO GRUPOS"
        self.visible_sprites.camera_draw()

        "Câmera centrada"
        # self.visible_sprites.camera_pursuer(self.player)

        "Câmera de borda + seu retângulo"
        self.visible_sprites.camera_window(self.player)
        # print(pygame.draw.rect(self.canvas, 'crimson', self.visible_sprites.camera_rect, 5))

    def setup_level(self, target_map):
        # Mapa lista de strings (settings)
        for row_index, row in enumerate(target_map):
            for col_index, col in enumerate(row):
                "print(f'{col_index}:{row}->{col_index * tile_size}')"
                "print(f'{row_index}:{row}->{row_index * tile_size}')"

                "CADA CONDIÇÃO INDICA 1 ITEM DO MAPA"
                if col == 'X':
                    # Localização da "posição" e dos "grupos" ao qual o PERSONAGEM e as PLATAFORMAS pertencerão
                    x, y = col_index * 64, row_index * 49

                    # Colisão pt1 - Adição das PLATAFORMAS e JOGADOR ao grupo dos sprites de colisão
                    "QUANDO AS SUPERFÍCIES FOREM IMAGENS ESCOLHIDAS ALEATORIAMENTE"
                    random_width = choice(tuple(range(50, 101)))
                    random_height = choice(tuple(range(50, 101)))
                    self.terrain = Tile(
                       pos=(x, y),
                       group=[self.visible_sprites, self.collision_sprites],
                       custom=False,
                       w=random_width,
                       h=random_height,
                       image_path=None
                    )

                    "QUANDO AS SUPERFÍCIES SÃO 1 IMAGEM ÚNICA"
                    # self.terrain = Tile(
                    #     pos=(x, y), group=[self.visible_sprites, self.collision_sprites], custom=True, w=64, h=49,
                    #     image_path='sprites/platforms/plat_2.gif')

                elif col == 'B':
                    x, y = col_index * 45, row_index * 45
                    self.stone_block = Tile(
                        pos=(x, y), group=[self.visible_sprites, self.collision_sprites], custom=True, w=32, h=32,
                        image_path='sprites/platforms/plat_4.gif'
                    )

                elif col == 'P':
                    x, y = col_index * 64, row_index * 49
                    # TODO: O grupo dos sprites de colisão não pertence ao do personagem
                    self.player = Player(
                        pos=(x, y), group=[self.visible_sprites, self.active_sprites],
                        collision_sprites=self.collision_sprites
                    )

                elif col == 'T':
                    x, y = col_index * 45, row_index * 45
                    self.wooden_box = Tile(
                        pos=(x, y), group=[self.visible_sprites, self.collision_sprites], custom=True, w=40, h=40,
                        image_path='sprites/platforms/plat_3.gif'
                    )

                elif col == 'E':
                    x, y = col_index * 45, row_index * 45
                    kind = ['shell_green', 'shell_purple']
                    width = [*range(18, 37)]
                    height = [*range(16, 33)]
                    self.shell = Enemy(
                        shell=choice(kind),
                        custom_size=True,
                        width_=36,
                        height_=32,
                        pos=(x, y),
                        group=[self.visible_sprites, self.active_sprites, self.collision_sprites],
                    )

    # Função usada apenas para printar códigos de teste no canvas
    def printer(self):
        # print(self.player.x, self.player.y)
        # print([1], self.visible_sprites.sprites())
        # print([2], self.active_sprites.sprites())
        # print([3], self.collision_sprites.sprites())
        # for index, sprite in enumerate(self.visible_sprites.sprites()):
        #     print([index], sprite.__dict__)
        # print(dir(self.active_sprites))
        # print(dir(self.visible_sprites))
        # print(dir(self.collision_sprites))
        pass


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.canvas = pygame.display.get_surface()

        self.offset = pygame.math.Vector2(100, 300)

        # Câmera centrada no personagem
        self.half_width = self.canvas.get_size()[0] // 2
        self.half_height = self.canvas.get_size()[1] // 2

        # Câmera de borda
        self.coords = {'left': 300, 'right': 300, 'top': 100, 'bottom': 150}
        top_ = self.coords['top']
        left_ = self.coords['left']
        width_ = self.canvas.get_size()[0] - (self.coords['left'] + self.coords['right'])
        height_ = self.canvas.get_size()[1] - (self.coords['top'] + self.coords['bottom'])
        self.camera_rect = pygame.Rect(left_, top_, width_, height_)

        # Imagens de fundo (x2) (desenhado em "camera_draw", antes do loop que desenha as plataformas)
        self.background = pygame.image.load('sprites/backgrounds/background.png').convert_alpha()
        self.background_rect = self.background.get_rect(center=(0, 0))
        self.background_vector = None
        self.hills = pygame.image.load('sprites/backgrounds/hills.png').convert_alpha()
        self.hills_rect = self.background.get_rect(center=(0, 0))
        self.hills_vector = None

    # Câmera centrada no personagem
    def camera_pursuer(self, target):
        self.offset.x = target.rect.centerx - self.half_width
        self.offset.y = target.rect.centery - self.half_height

    def camera_draw(self):
        # Desenho das imagens de fundo criadas na função "init" desta classe
        self.background_vector = self.background_rect.center - self.offset
        self.hills_vector = self.hills_rect.center - self.offset
        self.canvas.blit(self.background, self.background_vector)
        self.canvas.blit(self.hills, self.hills_vector)

        for index, sprite in enumerate(self.sprites()):
            "print([index], sprite.__dict__)"

            # Se não for "topleft", colisão fica bugada
            sprite_offset = sprite.rect.topleft - self.offset

            "ANTES DO VETOR (estático)"
            # self.canvas.blit(sprite.image, sprite.rect)

            "DEPOIS DO VETOR (tela em movimento)"
            self.canvas.blit(sprite.image, sprite_offset)

    # Câmera de borda
    def camera_window(self, target):
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left

        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.coords['left']
        self.offset.y = self.camera_rect.top - self.coords['top']
