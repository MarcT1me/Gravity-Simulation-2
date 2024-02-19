# graphics
import pygame

# core elements
from PhEngineV2.data import config


class Loading:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.value = 0
        self.image = pygame.transform.scale(
            pygame.image.load(
                rf'{config.APPLICATION_PATH}/core/presets/textures/loading_image.jpg'
            ), config.Screen.size
        )
        self.loading_font = pygame.font.SysFont('Arial', 50, bold=True).render(
            f'LOADING', True, (165, 42, 42)
        )
        self.percents_font = pygame.font.SysFont('Arial', 12, bold=True)

        self.draw_progress(0)

    def blit_image(self) -> None:
        """ Функция вывода изображения экрана загрузки """
        self.screen.blit(self.image, (0, 0))
        pygame.display.flip()
        self.screen.blit(
            self.loading_font,
            (config.Screen.half_size[0]//2 - self.loading_font.get_width()//2, config.Screen.half_size[1]//2)
        )

    def draw_progress(self, value) -> None:
        """ Функция вывода прогресса загрузки """
        self.value = value
        fin_percents_font = self.percents_font.render(
            f'{value} %', True, (255, 215, 0)
        )
        self.blit_image()
        self.screen.blit(fin_percents_font, (config.Screen.size[0] - 31, config.Screen.size[1] - 43))
        pygame.draw.rect(self.screen, (119, 136, 153),
                         (10, config.Screen.size[1] - 45, (config.Screen.size[0] - 61)/(100/(self.value + 1)), 20)
                         )
        pygame.display.flip()
