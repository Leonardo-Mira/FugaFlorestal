
import pygame
import os
from code import const


class Menu:

    def __init__(self, screen):

        self.screen = screen

        # Carrega a imagem de fundo
        image_path = os.path.join(
            const.ASSET_FOLDER,
            const.BACKGROUND_IMAGE
        )

        self.background = pygame.image.load(image_path).convert()

        self.background = pygame.transform.scale(
            self.background,
            (const.SCREEN_WIDTH, const.SCREEN_HEIGHT)
        )

        # Fontes do menu
        self.title_font = pygame.font.Font(None, 100)
        self.button_font = pygame.font.Font(None, 55)
        self.instruction_font = pygame.font.Font(None, 28)
        self.credit_font = pygame.font.Font(None, 24)

        # Botão Jogar
        self.play_button = pygame.Rect(
            const.SCREEN_WIDTH // 2 - 120,
            320,
            240,
            65
        )

        # Botão Sair
        self.exit_button = pygame.Rect(
            const.SCREEN_WIDTH // 2 - 120,
            405,
            240,
            65
        )

        # Opção selecionada
        # 0 = Jogar
        # 1 = Sair
        self.selected_option = 0

    def handle_events(self, event):

        # Navegação pelo teclado
        if event.type == pygame.KEYDOWN:

            # Alterna entre as opções
            if event.key in (pygame.K_UP, pygame.K_DOWN):

                self.selected_option = 1 - self.selected_option

            # Confirma a opção selecionada
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):

                if self.selected_option == 0:
                    return "play"

                else:
                    return "exit"

        # Seleção pelo mouse
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                if self.play_button.collidepoint(event.pos):
                    return "play"

                if self.exit_button.collidepoint(event.pos):
                    return "exit"

        return None

    def draw(self):

        # Desenha o fundo
        self.screen.blit(self.background, (0, 0))

        # Camada escura para destacar os textos
        overlay = pygame.Surface(
            (const.SCREEN_WIDTH, const.SCREEN_HEIGHT)
        )

        overlay.set_alpha(80)
        overlay.fill((0, 0, 0))

        self.screen.blit(overlay, (0, 0))

        # Título do jogo
        title = self.title_font.render(
            "FUGA FLORESTAL",
            True,
            (255, 255, 255)
        )

        title_rect = title.get_rect(
            center=(const.SCREEN_WIDTH // 2, 170)
        )

        self.screen.blit(title, title_rect)

        # Cores dos botões
        selected_color = (70, 160, 75)
        normal_color = (45, 120, 55)
        exit_color = (130, 45, 45)

        # Botão Jogar
        if self.selected_option == 0:
            play_color = selected_color
        else:
            play_color = normal_color

        pygame.draw.rect(
            self.screen,
            play_color,
            self.play_button,
            border_radius=12
        )

        # Destaque da opção selecionada
        if self.selected_option == 0:
            pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                self.play_button,
                3,
                border_radius=12
            )

        play_text = self.button_font.render(
            "JOGAR",
            True,
            (255, 255, 255)
        )

        play_rect = play_text.get_rect(
            center=self.play_button.center
        )

        self.screen.blit(play_text, play_rect)

        # Botão Sair
        if self.selected_option == 1:
            exit_color = (180, 65, 65)

        pygame.draw.rect(
            self.screen,
            exit_color,
            self.exit_button,
            border_radius=12
        )

        # Destaque da opção selecionada
        if self.selected_option == 1:
            pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                self.exit_button,
                3,
                border_radius=12
            )

        exit_text = self.button_font.render(
            "SAIR",
            True,
            (255, 255, 255)
        )

        exit_rect = exit_text.get_rect(
            center=self.exit_button.center
        )

        self.screen.blit(exit_text, exit_rect)

        # Instrução de navegação do menu
        menu_instruction = self.instruction_font.render(
            "Use as SETAS para selecionar e ENTER para confirmar",
            True,
            (255, 255, 255)
        )

        menu_rect = menu_instruction.get_rect(
            center=(const.SCREEN_WIDTH // 2, 525)
        )

        self.screen.blit(menu_instruction, menu_rect)

        # Instrução dos controles do jogo
        jump_instruction = self.instruction_font.render(
            "Pressione ESPAÇO para pular durante o jogo",
            True,
            (255, 255, 255)
        )

        jump_rect = jump_instruction.get_rect(
            center=(const.SCREEN_WIDTH // 2, 560)
        )

        self.screen.blit(jump_instruction, jump_rect)

        # Condição de vitória
        victory_instruction = self.instruction_font.render(
            "Alcance 30 metros para vencer!",
            True,
            (255, 255, 255)
        )

        victory_rect = victory_instruction.get_rect(
            center=(const.SCREEN_WIDTH // 2, 595)
        )

        self.screen.blit(victory_instruction, victory_rect)

        # Créditos do desenvolvedor
        credit = self.credit_font.render(
            "Desenvolvido por Leonardo Roberto de Mira | RU: 5518144",
            True,
            (255, 255, 255)
        )

        credit_rect = credit.get_rect(
            center=(const.SCREEN_WIDTH // 2, 690)
        )

        self.screen.blit(credit, credit_rect)
