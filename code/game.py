import pygame
from code import const


class Game:

    def __init__(self):
        # Inicialização do Pygame
        pygame.init()

        # Configuração da janela
        self.screen = pygame.display.set_mode(
            (const.SCREEN_WIDTH, const.SCREEN_HEIGHT)
        )

        pygame.display.set_caption(const.SCREEN_TITLE)

        # Controle de FPS
        self.clock = pygame.time.Clock()

        # Controle da execução
        self.running = True

    def handle_events(self):
        # Captura dos eventos
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        # Atualização dos elementos do jogo
        pass

    def draw(self):
        # Desenho dos elementos na tela
        self.screen.fill((30, 80, 45))

        pygame.display.flip()

    def run(self):
        # Loop principal do jogo
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            self.clock.tick(const.FPS)

        pygame.quit()
