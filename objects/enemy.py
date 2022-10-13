

import pygame
from random import choice


class Enemy(pygame.sprite.Sprite):
    """
    Enemy(
        shell=choice(kind),
        custom_size=False,
        width_=0,
        height_=0,
        pos=(choice(where), 600 - 61),
        group=[self.visible_sprites, self.collision_sprites]
    )
    """

    def __init__(self, shell, custom_size, width_, height_, pos, group):
        super().__init__(group)
        # Acessar o canvas de forma indireta (clone da var "screen")
        self.canvas = pygame.display.get_surface()

        self.x, self.y = pos[0], pos[1]

        # Var criada SOMENTE por haver uma variedade de inimigos
        self.shell = shell

        # Vars criadas SOMENTE se quiser que o inimigo tenha tamanho variado (tamanho 2x maior que as originais)
        self.proper_width = [*range(36, 51)]
        self.proper_height = [*range(32, 41)]

        # (True) p/ dimensões customizadas VS (False) p/ dimensões escolhidas pela classe
        self.custom_size = custom_size
        if self.custom_size:
            self.width_ = width_
            self.height_ = height_
            self.image = pygame.transform.scale(
                pygame.image.load('sprites\\shells\\green_shell_1_tr.gif'), (self.width_, self.height_)
            ).convert_alpha()
            self.rect = self.image.get_rect(center=pos)
        else:
            self.width_ = choice(self.proper_width)
            self.height_ = choice(self.proper_height)
            self.image = pygame.transform.scale(
                pygame.image.load('sprites\\shells\\green_shell_1_tr.gif'), (self.width_, self.height_)
            ).convert_alpha()
            self.rect = self.image.get_rect(center=pos)

        # Lista do path das imagens (range= qtd. de imagens criadas e índices que a lista terá)
        # As imagens mudam de nome apenas nos números, p/ facilitar o uso do "list comprehension"
        self.shells_green = [f'sprites\\shells\\green_shell_{index}_tr.gif' for index in range(1, 5)]
        self.shells_purple = [f'sprites\\shells\\purple_shell_{index}_tr.gif' for index in range(1, 5)]

        self.shells_variety = ['shell_green', 'shell_purple']
        self.shells_images = [self.shells_green, self.shells_purple]
        self.groups = len(self.shells_variety)

        # Vars que controlam a transição dos sprites criados acima e o tempo de transição delas
        # Vars usadas majoritariamente na função "sprite_admin"
        self.current_sprite_index = 0
        self.delay = 0

        # Vars que controlam a velocidade horizontal dos inimigos no canvas
        self.go_right = [*range(2, 8)]
        self.go_left = [*range(5, 11)]

    # "self.image" e "self.rect", definidos em "sprite_admin", são exibidos no Canvas por esta função
    def draw(self):
        self.canvas.blit(self.image, self.rect)

    # Usada na função "sprite_admin" p/ converter imagens p/ um tamanho customizado
    def resized_enemy(self, img):
        return pygame.transform.scale(img, (self.width_, self.height_))

    # Atribuição das vars das imagens e de seus retângulos com base em "self.current_sprite_index"
    # "self.delay" controla quando "self.current_sprite_index" deve mudar seu valor
    # Lógica: se "self.current_sprite_index=2", exibirá o sprite "2" do seu grupo de sprites
    # O grupo de sprites não faz movimentos uniformas, pois o atraso não é um valor único (choice)
    def sprite_admin_enemy(self):
        self.delay += 1
        if self.delay % choice([*range(2, 11)]) == 0:
            self.current_sprite_index += 1

        "LOOP REDUZIDO PARA EVITAR REPETIÇÃO DE CÓDIGO"
        for group_index, group in enumerate(range(self.groups)):
            if self.shell == self.shells_variety[group_index]:
                for index, each_image in enumerate(self.shells_images[group_index]):
                    if self.current_sprite_index == index:
                        self.image = self.resized_enemy(pygame.image.load(each_image).convert_alpha())
                        self.rect = self.image.get_rect(center=self.rect.center)
                    if self.current_sprite_index > len(self.shells_images[group_index]):
                        self.current_sprite_index = 0

        "CÓDIGO ANTIGO"
        # if self.shell == 'shell_green':
        #     for index, each_image in enumerate(self.shells_green):
        #         if self.current_sprite_index == index:
        #             self.image = self.resized_enemy(pygame.image.load(each_image).convert_alpha())
        #             self.rect = self.image.get_rect(center=self.rect.center)
        #         if self.current_sprite_index > len(self.shells_green):
        #             self.current_sprite_index = 0
        # elif self.shell == 'shell_purple':
        #     for index, each_image in enumerate(self.shells_purple):
        #         if self.current_sprite_index == index:
        #             self.image = self.resized_enemy(pygame.image.load(each_image).convert_alpha())
        #             self.rect = self.image.get_rect(center=self.rect.center)
        #         if self.current_sprite_index > len(self.shells_purple):
        #             self.current_sprite_index = 0

    # Pega o retângulo de cada imagem e os movimenta horizontalmente e lateralmente
    def move(self):
        self.rect.right += choice(self.go_right)
        self.rect.left -= choice(self.go_left)

    # TODO 10.1: Detecta colisão do retângulo do inimigo com o do personagem (no loop do Pygame, é usado em loop)
    def enemy_collision(self, player_rectangle):
        if self.rect.colliderect(player_rectangle):
            # print('ouch')
            pygame.draw.rect(self.canvas, 'cyan', player_rectangle, 10)
            return True
        else:
            return ''

    def update(self):
        self.sprite_admin_enemy()
        self.draw()
        self.move()
