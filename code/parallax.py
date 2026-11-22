
import pygame
import os
from code import const


class Parallax:

    def __init__(self, screen):

        self.screen = screen

        # Carregamento das camadas
        self.sky = self.load_image(const.SKY_IMAGE)
        self.bg_decor = self.load_image(const.BG_DECOR_IMAGE)
        self.middle_decor = self.load_image(const.MIDDLE_DECOR_IMAGE)
        self.foreground = self.load_image(const.FOREGROUND_IMAGE)
        self.ground = self.load_image(const.GROUND_IMAGE)

        # Velocidade de cada camada
        self.layers = [
            [self.sky, 0.2, 0],
            [self.bg_decor, 0.5, 0],
            [self.middle_decor, 1.2, 0],
            [self.foreground, 2.5, 0],
            [self.ground, 6.0, 0]
        ]

    def load_image(self, image_name):

        image_path = os.path.join(
            const.ASSET_FOLDER,
            image_name
        )

        image = pygame.image.load(image_path).convert_alpha()

        return pygame.transform.scale(
            image,
            (const.SCREEN_WIDTH, const.SCREEN_HEIGHT)
        )

    def update(self):

        for layer in self.layers:

            image, speed, offset = layer

            width = image.get_width()

            # Atualiza a posição horizontal
            offset = (offset + speed) % width

            layer[2] = offset

    def draw(self):

        for image, speed, offset in self.layers:

            width = image.get_width()

            # Desenha duas cópias para criar continuidade
            self.screen.blit(image, (-offset, 0))
            self.screen.blit(image, (width - offset, 0))
