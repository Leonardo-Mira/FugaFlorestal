
import pygame
import os
from code import const


class Player:

    def __init__(self):

        # Carrega as animações
        self.run_frames = self.load_frames("Player_Running", 12)
        self.jump_start_frames = self.load_frames("Player_Jump_Start", 6)
        self.jump_loop_frames = self.load_frames("Player_Jump_Loop", 6)

        # Carrega o som do pulo
        jump_sound_path = os.path.join(
            const.ASSET_FOLDER,
            const.JUMP_SOUND
        )

        self.jump_sound = pygame.mixer.Sound(jump_sound_path)
        self.jump_sound.set_volume(0.5)

        # Controle da animação
        self.current_animation = "run"
        self.current_frame = 0
        self.animation_timer = 0

        # Velocidade das animações
        self.run_animation_speed = 0.25
        self.jump_animation_speed = 0.18

        # Posição do personagem
        self.x = 150
        self.y = const.SCREEN_HEIGHT - 250
        self.ground_y = self.y

        # Controle do pulo
        self.is_jumping = False
        self.velocity_y = 0

    def load_frames(self, prefix, frame_count):

        frames = []

        for i in range(frame_count):

            image_name = f"{prefix}_{i:03}.png"

            image_path = os.path.join(
                const.ASSET_FOLDER,
                image_name
            )

            image = pygame.image.load(image_path).convert_alpha()

            # Ajusta o tamanho do personagem
            original_width, original_height = image.get_size()

            new_height = 300
            new_width = int(
                original_width * (new_height / original_height)
            )

            image = pygame.transform.scale(
                image,
                (new_width, new_height)
            )

            frames.append(image)

        return frames

    def jump(self):

        if not self.is_jumping:

            self.is_jumping = True
            self.velocity_y = const.PLAYER_JUMP_STRENGTH

            # Reproduz o som do pulo
            self.jump_sound.play()

            self.current_animation = "jump_start"
            self.current_frame = 0
            self.animation_timer = 0

    def update(self):

        # Atualiza a física do pulo
        if self.is_jumping:

            self.y += self.velocity_y
            self.velocity_y += const.GRAVITY

            # Verifica a aterrissagem
            if self.y >= self.ground_y:

                self.y = self.ground_y
                self.is_jumping = False
                self.velocity_y = 0

                # Reinicia a animação de corrida
                self.current_animation = "run"
                self.current_frame = 0
                self.animation_timer = 0

        # Define os frames e a velocidade da animação
        if self.current_animation == "run":

            frames = self.run_frames
            animation_speed = self.run_animation_speed

        elif self.current_animation == "jump_start":

            frames = self.jump_start_frames
            animation_speed = self.jump_animation_speed

        else:

            frames = self.jump_loop_frames
            animation_speed = self.jump_animation_speed

        # Atualiza a animação
        self.animation_timer += animation_speed

        while self.animation_timer >= 1:

            self.animation_timer -= 1
            self.current_frame += 1

            # Passa da preparação para o pulo no ar
            if self.current_animation == "jump_start":

                if self.current_frame >= len(self.jump_start_frames):

                    self.current_animation = "jump_loop"
                    self.current_frame = 0
                    self.animation_timer = 0

            # Repete as demais animações
            else:

                if self.current_frame >= len(frames):

                    self.current_frame = 0

    def draw(self, screen):

        # Seleciona a imagem atual
        if self.current_animation == "run":

            image = self.run_frames[self.current_frame]

        elif self.current_animation == "jump_start":

            image = self.jump_start_frames[self.current_frame]

        else:

            image = self.jump_loop_frames[self.current_frame]

        screen.blit(image, (self.x, self.y))

    def get_collision_rect(self):

        # Identifica a imagem atual
        if self.current_animation == "run":
            image = self.run_frames[self.current_frame]

        elif self.current_animation == "jump_start":
            image = self.jump_start_frames[self.current_frame]

        else:
            image = self.jump_loop_frames[self.current_frame]

        # Obtém a área visível da imagem
        rect = image.get_bounding_rect()

        rect.x += self.x
        rect.y += self.y

        # Reduz a área de colisão
        rect.inflate_ip(-50, -50)

        return rect
