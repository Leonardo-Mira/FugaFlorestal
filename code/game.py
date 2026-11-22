
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

        # Fontes das mensagens
        self.game_over_font = pygame.font.Font(None, 90)
        self.restart_font = pygame.font.Font(None, 40)
        self.distance_font = pygame.font.Font(None, 42)

        # Controle de FPS
        self.clock = pygame.time.Clock()

        # Controle da execução
        self.running = True
        self.game_over = False
        self.victory = False

        # Inicializa os elementos da partida
        self.reset_game()

    def reset_game(self):

        # Reinicia o cenário
        self.parallax = Parallax(self.screen)

        # Reinicia o personagem
        self.player = Player()

        # Reinicia os obstáculos
        self.obstacle_manager = ObstacleManager()

        # Reinicia a distância
        self.distance = 0

        # Reinicia os estados da partida
        self.game_over = False
        self.victory = False

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:

                # Pulo do personagem
                if event.key == pygame.K_SPACE and not self.game_over and not self.victory:
                    self.player.jump()

                # Reinicia a partida
                if event.key == pygame.K_r and (self.game_over or self.victory):
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
        if not self.game_over and not self.victory:

            # Atualiza o cenário
            self.parallax.update()

            # Atualiza o personagem
            self.player.update()

            # Atualiza os obstáculos
            self.obstacle_manager.update()

            # Atualiza a distância percorrida
            self.distance += 0.025

            # Verifica colisões
            self.check_collision()

            # Verifica se alcançou a distância final
            if not self.game_over and self.distance >= const.TARGET_DISTANCE:

                self.victory = True

    def draw(self):

        # Desenha o cenário
        self.parallax.draw()

        # Desenha os obstáculos
        self.obstacle_manager.draw(self.screen)

        # Desenha o personagem
        self.player.draw(self.screen)

        # Mostra a distância percorrida
        distance_text = self.distance_font.render(
            f"Distância: {int(self.distance)} m",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            distance_text,
            (30, 25)
        )

        # Mostra Game Over ou Vitória
        if self.game_over or self.victory:

            overlay = pygame.Surface(
                (const.SCREEN_WIDTH, const.SCREEN_HEIGHT)
            )

            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))

            self.screen.blit(overlay, (0, 0))

            # Define a mensagem conforme o resultado
            if self.victory:
                message = "VOCE VENCEU!"
            else:
                message = "GAME OVER"

            text = self.game_over_font.render(
                message,
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
