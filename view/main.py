import pygame as pg
from view.constants import WHITE_COLOR, GRAY_COLOR, PEACH_COLOR, WIDTH, HEIGHT
from view.buttons import Button, Text
pg.init()


class SceneRender:
    def __init__(self):
        self.__buttons = {
            'start_button': Button((WIDTH // 2, HEIGHT // 1.75),
                                   'START', (WIDTH // 3.8, HEIGHT // 10),
                                   round((WIDTH + HEIGHT) // 31))
        }
        self.__text = {
            'caption': Text((WIDTH // 2, HEIGHT // 9),
                            'Capybarun',
                            round((WIDTH + HEIGHT) // 20))
        }
        self.__background = self.create_background()

    def render_menu(self, screen: pg.Surface):
        screen.blit(self.__background, (0, 0))
        self.__buttons['start_button'].render(screen)
        self.__text['caption'].render(screen)
        pg.display.update()

    def render_game(self, screen: pg.Surface):
        screen.fill(PEACH_COLOR)
        pg.display.update()

    def render_maze(self, screen: pg.Surface):
        screen.blit(self.__background, (0, 0))
        pg.display.update()

    def render_final(self, screen: pg.Surface):
        pass

    def get_buttons(self) -> dict:
        return self.__buttons

    def create_background(self):
        path_to_background = 'view/sprites/Background.png'
        background_image = pg.image.load(path_to_background).convert()
        background_image = pg.transform.scale(background_image, (WIDTH, HEIGHT))
        return background_image