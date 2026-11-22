
import pygame
import os
import random
from code import const


class ObstacleManager:

    def __init__(self):

        # Lista que armazenará os obstáculos ativos
        self.obstacles = []

        # Carrega as imagens dos obstáculos
        self.images = []

        obstacle_names = [
            "Object2.png",
            "Object3.png",
            "Object6.png",
            "Object8.png"
        ]

        for image_name in obstacle_names:

            image_path = os.path.join(
                const.ASSET_FOLDER,
                image_name
            )

            image = pygame.image.load(image_path).convert_alpha()

            # Ajusta o tamanho do obstáculo
            original_width, original_height = image.get_size()

            new_height = 90
            new_width = int(
                original_width * (new_height / original_height)
            )

            image = pygame.transform.scale(
                image,
                (new_width, new_height)
            )

            self.images.append(image)

        # Controle do tempo de aparecimento
        self.spawn_timer = 0
        self.spawn_interval = 120

    def spawn(self):

        # Escolhe um obstáculo aleatório
        image = random.choice(self.images)

        # Cria o obstáculo fora da tela, à direita
        x = const.SCREEN_WIDTH

        y = const.SCREEN_HEIGHT - image.get_height() - 5

        obstacle = {
            "image": image,
            "x": x,
            "y": y
        }

        self.obstacles.append(obstacle)

    def update(self):

        # Controla o aparecimento dos obstáculos
        self.spawn_timer += 1

        if self.spawn_timer >= self.spawn_interval:

            self.spawn()
            self.spawn_timer = 0

        # Move os obstáculos para a esquerda
        for obstacle in self.obstacles:

            obstacle["x"] -= const.OBSTACLE_SPEED

        # Remove obstáculos que saíram da tela
        self.obstacles = [
            obstacle
            for obstacle in self.obstacles
            if obstacle["x"] + obstacle["image"].get_width() > 0
        ]

    def draw(self, screen):

        # Desenha todos os obstáculos
        for obstacle in self.obstacles:

            screen.blit(
                obstacle["image"],
                (obstacle["x"], obstacle["y"])
            )
