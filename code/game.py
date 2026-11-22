
import pygame
from code import const
from code.menu import Menu
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
        self.game_started = False
        self.game_over = False
        self.victory = False

        # Inicializa o menu
        self.menu = Menu(self.screen)

        # Opções das telas de resultado
        self.result_font = pygame.font.Font(None, 45)
        self.selected_result_option = 0

        self.restart_button = pygame.Rect(
            const.SCREEN_WIDTH // 2 - 180,
            390,
            360,
            60
        )

        self.menu_button = pygame.Rect(
            const.SCREEN_WIDTH // 2 - 180,
            470,
            360,
            60
        )

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

        # Seleciona a primeira opção
        self.selected_result_option = 0

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            # Eventos do menu inicial
            if not self.game_started:

                action = self.menu.handle_events(event)

                if action == "play":
                    self.reset_game()
                    self.game_started = True

                elif action == "exit":
                    self.running = False

            # Eventos durante a partida
            else:

                # Eventos da tela de Game Over ou Vitória
                if self.game_over or self.victory:

                    if event.type == pygame.KEYDOWN:

                        # Navegação entre as opções
                        if event.key in (pygame.K_UP, pygame.K_DOWN):

                            self.selected_result_option = (
                                1 - self.selected_result_option
                            )

                        # Confirma a opção selecionada
                        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):

                            if self.selected_result_option == 0:

                                # Reinicia a partida
                                self.reset_game()

                            else:

                                # Volta para o menu
                                self.reset_game()
                                self.game_started = False
                                self.menu.selected_option = 0

                    # Seleção pelo mouse
                    if event.type == pygame.MOUSEBUTTONDOWN:

                        if event.button == 1:

                            if self.restart_button.collidepoint(event.pos):

                                self.reset_game()

                            elif self.menu_button.collidepoint(event.pos):

                                self.reset_game()
                                self.game_started = False
                                self.menu.selected_option = 0

                # Eventos durante a partida ativa
                else:

                    if event.type == pygame.KEYDOWN:

                        # Pulo do personagem
                        if event.key == pygame.K_SPACE:
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
        if self.game_started and not self.game_over and not self.victory:

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

    def draw_result_button(self, button, text, selected):

        # Define a cor do botão
        if selected:
            color = (70, 160, 75)
        else:
            color = (45, 120, 55)

        # Desenha o botão
        pygame.draw.rect(
            self.screen,
            color,
            button,
            border_radius=12
        )

        # Destaca a opção selecionada
        if selected:

            pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                button,
                3,
                border_radius=12
            )

        # Desenha o texto
        button_text = self.result_font.render(
            text,
            True,
            (255, 255, 255)
        )

        button_rect = button_text.get_rect(
            center=button.center
        )

        self.screen.blit(button_text, button_rect)

    def draw(self):

        # Mostra o menu inicial
        if not self.game_started:

            self.menu.draw()

        else:

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
                    message = "VOCÊ VENCEU!"
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
                        290
                    )
                )

                self.screen.blit(text, text_rect)

                # Botão Jogar Novamente
                self.draw_result_button(
                    self.restart_button,
                    "JOGAR NOVAMENTE",
                    self.selected_result_option == 0
                )

                # Botão Voltar ao Menu
                self.draw_result_button(
                    self.menu_button,
                    "VOLTAR AO MENU",
                    self.selected_result_option == 1
                )

                # Instrução de navegação
                instruction = self.distance_font.render(
                    "Use as SETAS para selecionar e ENTER para confirmar",
                    True,
                    (255, 255, 255)
                )

                instruction_rect = instruction.get_rect(
                    center=(
                        const.SCREEN_WIDTH // 2,
                        570
                    )
                )

                self.screen.blit(instruction, instruction_rect)

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
