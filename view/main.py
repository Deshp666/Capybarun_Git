import pygame as pg
from view.constants import WHITE_COLOR, GRAY_COLOR, PEACH_COLOR, WIDTH, HEIGHT, SWAMP_COLOR, DEEP_GREEN_COLOR,\
    MAZE_HEIGHT, MAZE_WIDTH, CAPTION
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
                            CAPTION,
                            round((WIDTH + HEIGHT) // 20))
        }
        self.__background = self.create_background()

    def render_menu_scene(self, screen: pg.Surface):
        self.render_background(screen)
        self.__buttons['start_button'].render(screen)
        self.__text['caption'].render(screen)
        pg.display.update()

    def render_game_scene(self, screen: pg.Surface):
        screen.fill(PEACH_COLOR)
        pg.display.update()

    def render_maze_scene(self, screen: pg.Surface, time_to_print: str, maze: list[pg.Rect]):
        self.render_background(screen)
        self.render_maze(screen, maze)
        #self.render_player_icon_maze(screen)
        self.render_timer(screen, time_to_print)
        pg.display.update()

    def render_final_scene(self, screen: pg.Surface):
        screen.fill(GRAY_COLOR)
        pg.display.update()

    def get_buttons(self) -> dict:
        return self.__buttons

    def render_maze(self, screen: pg.Surface, maze: list[pg.Rect]):
        background = self.create_background_for_maze()
        screen.blit(background, (WIDTH // 18, HEIGHT // 18))
        for rect in maze:
            pg.draw.rect(screen, PEACH_COLOR, rect)

    def render_player_icon_maze(self, screen: pg.Surface, x: int, y: int):
        pg.draw.rect(screen, GRAY_COLOR, rect)

    def render_timer(self, screen: pg.Surface, time_to_print: str):
        text = Text((WIDTH // 1.1494, HEIGHT // 25.714),
                    time_to_print,
                    (WIDTH + HEIGHT) // 45,
                    SWAMP_COLOR)
        text.render(screen)

    def render_background(self, screen: pg.Surface):
        screen.blit(self.__background, (0, 0))

    def create_background(self) -> pg.Surface:
        path_to_background = 'view/sprites/Background.png'
        background_image = pg.image.load(path_to_background).convert()
        background_image = pg.transform.scale(background_image, (WIDTH, HEIGHT))
        return background_image

    def create_background_for_maze(self) -> pg.Surface:
        image = pg.Surface((WIDTH // 1.125, HEIGHT // 1.125))
        image.fill(DEEP_GREEN_COLOR)
        return image
