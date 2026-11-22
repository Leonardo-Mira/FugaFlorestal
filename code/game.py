
import pygame
from code import const
from code.parallax import Parallax


class Game:

    def __init__(self):

        # Inicialização do Pygame
        pygame.init()

        # Configuração da janela
        self.screen = pygame.display.set_mode(
            (const.SCREEN_WIDTH, const.SCREEN_HEIGHT)
        )

        pygame.display.set_caption(const.SCREEN_TITLE)

        # Inicialização do cenário Parallax
        self.parallax = Parallax(self.screen)

        # Controle de FPS
        self.clock = pygame.time.Clock()

        # Controle da execução
        self.running = True

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

    def update(self):

        # Atualiza o cenário Parallax
        self.parallax.update()

    def draw(self):

        # Desenha o cenário Parallax
        self.parallax.draw()

        pygame.display.flip()

    def run(self):

        while self.running:

            self.handle_events()
            self.update()
            self.draw()

            self.clock.tick(const.FPS)

        pygame.quit()
