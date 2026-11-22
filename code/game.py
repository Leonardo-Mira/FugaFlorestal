
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

        # Fonte das mensagens
        self.game_over_font = pygame.font.Font(None, 90)
        self.restart_font = pygame.font.Font(None, 40)

        # Controle de FPS
        self.clock = pygame.time.Clock()

        # Controle da execução
        self.running = True
        self.game_over = False

        # Inicializa os elementos da partida
        self.reset_game()

    def reset_game(self):

        # Reinicia o cenário
        self.parallax = Parallax(self.screen)

        # Reinicia o personagem
        self.player = Player()

        # Reinicia os obstáculos
        self.obstacle_manager = ObstacleManager()

        # Remove o estado de Game Over
        self.game_over = False

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:

                # Pulo do personagem
                if event.key == pygame.K_SPACE and not self.game_over:
                    self.player.jump()

                # Reinicia a partida
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()

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

            # Mensagem principal
            text = self.game_over_font.render(
                "GAME OVER",
                True,
                (255, 255, 255)
            )

            text_rect = text.get_rect(
                center=(
                    const.SCREEN_WIDTH // 2,
                    const.SCREEN_HEIGHT // 2 - 30
                )
            )

            self.screen.blit(text, text_rect)

            # Instrução para reiniciar
            restart_text = self.restart_font.render(
                "Pressione R para jogar novamente",
                True,
                (255, 255, 255)
            )

            restart_rect = restart_text.get_rect(
                center=(
                    const.SCREEN_WIDTH // 2,
                    const.SCREEN_HEIGHT // 2 + 40
                )
            )

            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def run(self):

        while self.running:

            self.handle_events()

            self.update()

            self.draw()

            # Controle de FPS
            self.clock.tick(const.FPS)

            # Exibe o FPS no título da janela
            fps = self.clock.get_fps()

            pygame.display.set_caption(
                f"{const.SCREEN_TITLE} - FPS: {fps:.1f}"
            )

        pygame.quit()
