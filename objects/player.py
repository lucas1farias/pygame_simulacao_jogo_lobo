

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites):
        super().__init__(group)
        self.sizes = (50, 50)

        "QUANDO O JOGADOR É UMA SUPERFÍCIE PYGAME"
        # self.player_color = '#C4f7FF'
        # self.image = pygame.Surface((tile_size / 2, tile_size))
        # self.image.fill(self.player_color)

        "QUANDO O JOGADOR POSSUI UM SPRITE (SPRITE INICIAL OBRIGATÓRIO)"
        self.image = pygame.transform.scale(
            pygame.image.load('sprites/player/wolf_idle_right_1_tr.png'), (self.sizes[0], self.sizes[1])
        ).convert_alpha()

        # "pos" definido em: "Level/setup_level/self.player"
        self.x, self.y = pos[0], pos[1]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Horizontal
        self.direction = pygame.math.Vector2()
        self.speed = 7

        # Vertical
        self.jump_speed = 20
        self.gravity = 1

        # Quando for desejado o PERSONAGEM colida com PLATAFORMAS
        self.collision_sprites = collision_sprites

        # Permitir o jogador saltar quando estiver no chão (impedir saltos múltiplos)
        self.on_floor = False

        self.current_sprite_index = 0

        self.controls = {
            'key': {
                'going_right': False,
                'going_left': False,
                'right': True,
                'left': False
            }
        }

    # Movimentação do vetor (movimentam o retângulo (na prática) horizontalmente em "update")
    def joystick(self):
        is_pressed = pygame.key.get_pressed()

        # Salto, a queda está em "add_gravity"
        if is_pressed[pygame.K_w] and self.on_floor:
            self.direction.y = -self.jump_speed

        # Horizontal em movimento
        if is_pressed[pygame.K_d]:
            self.direction.x = 1
            self.walk_right_setup()
        elif is_pressed[pygame.K_a]:
            self.direction.x = -1
            self.walk_left_setup()
        # Parada
        else:
            self.direction.x = 0

    # A classe "Player" está importada em: "Level/setup_level" e recebe o grupo "self.visible_sprites"
    # Em "Level/run", o grupo que influencia "Player" usa a função "update"
    # A função "Player/update" é usada lá, pelo vinculo de "Player" com grupos (par2)
    def update(self):
        self.sprite_admin()
        self.joystick()
        self.rect.x += self.direction.x * self.speed
        # A ordem aqui deve ser essa
        self.collision_horizontal()
        self.add_gravity()
        self.collision_vertical()

    def add_gravity(self):
        # Queda
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def collision_horizontal(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                # Se o personagem vêm da <- (vetor == -1), seu rect <- ocupa == rect alvo a ->
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                # Se o personagem vêm da -> (vetor == 1), seu rect -> ocupa == rect alvo a <-
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left

    def collision_vertical(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                # Quando o JOGADOR cai (vetor se torna 1)
                if self.direction.y > 0:
                    # Seu retângulo no FUNDO ocupa o mesmo ponto do TOPO do retângulo
                    self.rect.bottom = sprite.rect.top
                    # TODO: Parar de incrementar em "add_gravity"
                    self.direction.y = 0
                    # TODO: Impedimento de saltos múltiplos em contato com uma plataforma
                    self.on_floor = True

                # Quando o JOGADOR salta (vetor se torna -1)
                if self.direction.y < 0:
                    # Seu retângulo no TOPO ocupa o mesmo ponto do FUNDO do retângulo
                    self.rect.top = sprite.rect.bottom
                    # TODO: Queda imediata após colisão do TOPO com FUNDO
                    self.direction.y = 0

        # TODO: Impedir saltos múltiplos no ar (se pulou de cima, ou caiu de uma plataforma)
        if self.on_floor and self.direction.y != 0:
            self.on_floor = False

    def resized(self, the_image):
        return pygame.transform.scale(the_image, self.sizes)

    def sprite_admin(self,):
        # Ver exemplo abaixo, acima da condição 1
        frames = {
            'idle_right': [*range(7)],
            'idle_left': [*range(7)],
            'walk_right': [*range(9)],
            'walk_left': [*range(9)],
        }

        # Lista de inteiros convertidos p/ string para uso dentro das strings do "path" de cada imagem
        # Todos começam com 1, pois o número da primeira imagem é 1 (ex: "green_shell_1_tr.gif")
        # O último índice do range = último número da imagem, -1 (ex: "green_shell_8_tr.gif") = imagem 7
        frames_str = {
            'idle_right': [str(integer) for integer in range(1, 8)],
            'idle_left': [str(integer) for integer in range(1, 8)],
            'walk_right': [str(integer) for integer in range(1, 10)],
            'walk_left': [str(integer) for integer in range(1, 10)]
        }

        self.current_sprite_index += 1

        "========== EXEMPLO =========="
        "frames['idle_right']     = [0, 1, 2, 3, 4, 5, 6]"
        "frames_str['idle_right'] = ['1', '2', '3', '4', '5', '6', '7']"
        # SUPOSIÇÃO || se "self.current_sprite_index = 3", acessa "frames_str['idle_right'][3] = '4'"
        # ENTÃO     || f"sprites/wolf_idle_right_4_tr.png" ('4' inserido ao path da string)
        if self.controls['key']['right']:
            for index in range(len(frames['idle_right'])):
                if self.current_sprite_index == frames['idle_right'][index]:
                    self.image = self.resized(pygame.image.load(
                        f"sprites/player/wolf_idle_right_{frames_str['idle_right'][index]}_tr.png").convert_alpha())
                    self.rect = self.image.get_rect(center=self.rect.center)
                if self.current_sprite_index > len(frames['idle_right']):
                    self.current_sprite_index = 0

        if self.controls['key']['left']:
            for index in range(len(frames['idle_left'])):
                if self.current_sprite_index == frames['idle_left'][index]:
                    self.image = self.resized(pygame.image.load(
                        f"sprites/player/wolf_idle_left_{frames_str['idle_left'][index]}_tr.png").convert_alpha())
                    self.rect = self.image.get_rect(center=self.rect.center)
                if self.current_sprite_index > len(frames['idle_left']):
                    self.current_sprite_index = 0

        if self.controls['key']['going_right']:
            for index in range(len(frames['walk_right'])):
                if self.current_sprite_index == frames['walk_right'][index]:
                    self.image = self.resized(pygame.image.load(
                        f"sprites/player/wolf_walk_right_{frames_str['walk_right'][index]}_tr.png").convert_alpha())
                    self.rect = self.image.get_rect(center=self.rect.center)
                if self.current_sprite_index > len(frames['walk_right']):
                    self.current_sprite_index = 0

        if self.controls['key']['going_left']:
            for index in range(len(frames['walk_left'])):
                if self.current_sprite_index == frames['walk_left'][index]:
                    self.image = self.resized(pygame.image.load(
                        f"sprites/player/wolf_walk_left_{frames_str['walk_left'][index]}_tr.png").convert_alpha())
                    self.rect = self.image.get_rect(center=self.rect.center)
                if self.current_sprite_index > len(frames['walk_left']):
                    self.current_sprite_index = 0

    def idle_right_setup(self):
        self.controls['key']['going_left'] = False
        self.controls['key']['going_right'] = False
        self.controls['key']['left'] = False
        self.controls['key']['right'] = True

    def idle_left_setup(self):
        self.controls['key']['going_right'] = False
        self.controls['key']['going_left'] = False
        self.controls['key']['right'] = False
        self.controls['key']['left'] = True

    def walk_right_setup(self):
        self.controls['key']['right'] = False
        self.controls['key']['left'] = False
        self.controls['key']['going_left'] = False
        self.controls['key']['going_right'] = True

    def walk_left_setup(self):
        self.controls['key']['right'] = False
        self.controls['key']['left'] = False
        self.controls['key']['going_right'] = False
        self.controls['key']['going_left'] = True
