
import pygame
from code import const
from code.parallax import Parallax
from code.player import Player
from code.obstacle import ObstacleManager


class Game:

    def __init__(self):

        # Inicialização do Pygame
        pygame.init()

        # Configuração da janela
        self.screen = pygame.display.set_mode(
            (const.SCREEN_WIDTH, const.SCREEN_HEIGHT)
        )

        pygame.display.set_caption(const.SCREEN_TITLE)

        # Inicialização do cenário
        self.parallax = Parallax(self.screen)

        # Inicialização do personagem
        self.player = Player()

        # Inicialização dos obstáculos
        self.obstacle_manager = ObstacleManager()

        # Fonte da mensagem de Game Over
        self.game_over_font = pygame.font.Font(None, 90)

        # Controle de FPS
        self.clock = pygame.time.Clock()

        # Controle da execução
        self.running = True
        self.game_over = False

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and not self.game_over:
                    self.player.jump()

    def check_collision(self):

        # Área de colisão do personagem
        player_rect = self.player.get_collision_rect()

        # Verifica cada obstáculo
        for obstacle in self.obstacle_manager.obstacles:

            image = obstacle["image"]

            obstacle_rect = image.get_bounding_rect()

            obstacle_rect.x += obstacle["x"]
            obstacle_rect.y += obstacle["y"]

            # Reduz a área de colisão do obstáculo
            obstacle_rect.inflate_ip(-50, -50)

            # Verifica se houve colisão
            if player_rect.colliderect(obstacle_rect):

                self.game_over = True
                break

    def update(self):

        # Atualiza o jogo somente enquanto estiver ativo
        if not self.game_over:

            # Atualiza o cenário
            self.parallax.update()

            # Atualiza o personagem
            self.player.update()

            # Atualiza os obstáculos
            self.obstacle_manager.update()

            # Verifica colisões
            self.check_collision()

    def draw(self):

        # Desenha o cenário
        self.parallax.draw()

        # Desenha os obstáculos
        self.obstacle_manager.draw(self.screen)

        # Desenha o personagem
        self.player.draw(self.screen)

        # Mostra Game Over
        if self.game_over:

            overlay = pygame.Surface(
                (const.SCREEN_WIDTH, const.SCREEN_HEIGHT)
            )

            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))

            self.screen.blit(overlay, (0, 0))

            text = self.game_over_font.render(
                "GAME OVER",
                True,
                (255, 255, 255)
            )

            text_rect = text.get_rect(
                center=(
                    const.SCREEN_WIDTH // 2,
                    const.SCREEN_HEIGHT // 2
                )
            )

            self.screen.blit(text, text_rect)

        pygame.display.flip()


    def run(self):

        while self.running:

            self.handle_events()

            self.update()

            self.draw()

            self.clock.tick(const.FPS)

            # Obtém o FPS atual
            fps = self.clock.get_fps()

            # Exibe o FPS no título da janela
            pygame.display.set_caption(
                f"{const.SCREEN_TITLE} - FPS: {fps:.1f}"
            )

        pygame.quit()
