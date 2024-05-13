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
        self.__player_in_maze_icon = self.create_player_icon_in_maze()
        self.__prize_icon = self.create_prize_icon()

    def render_menu_scene(self, screen: pg.Surface):
        self.render_background(screen)
        self.__buttons['start_button'].render(screen)
        self.__text['caption'].render(screen)
        pg.display.update()

    def render_game_scene(self, screen: pg.Surface):
        screen.fill(PEACH_COLOR)
        pg.display.update()

    def render_maze_scene(self, screen: pg.Surface,
                          time_to_print: str,
                          maze_boundaries: list[pg.Rect],
                          maze_size: tuple[int, int],
                          player_in_maze_rect: tuple[pg.Rect, bool],
                          prize_rect: pg.Rect):
        self.render_background(screen)
        self.render_maze(screen, maze_boundaries, maze_size)
        self.render_player_icon_maze(screen, player_in_maze_rect)
        self.render_prize(screen, prize_rect)
        self.render_timer(screen, time_to_print)
        pg.display.update()

    def render_prize(self, screen: pg.Surface, rect: pg.Rect):
        x = rect.x
        y = rect.y
        width = rect.width
        height = rect.height
        icon = pg.transform.scale(self.__prize_icon,(width, height))
        screen.blit(icon, (x, y))

    def render_final_scene(self, screen: pg.Surface):
        screen.fill(GRAY_COLOR)
        pg.display.update()

    def get_buttons(self) -> dict:
        return self.__buttons

    def render_maze(self, screen: pg.Surface, maze_boundaries: list[pg.Rect], maze_size: tuple[int, int]):
        background = self.create_background_for_maze(maze_size)
        screen.blit(background, (WIDTH // 18, HEIGHT // 18))
        for rect in maze_boundaries:
            pg.draw.rect(screen, PEACH_COLOR, rect)

    def render_player_icon_maze(self, screen: pg.Surface, player_in_maze_rect: tuple[pg.Rect, bool]):
        player_rect = player_in_maze_rect[0]
        looking_right = player_in_maze_rect[1]
        width = player_rect.width
        height = player_rect.height
        x = player_rect.x
        y = player_rect.y
        icon = pg.transform.scale(self.__player_in_maze_icon, (width, height))
        if looking_right is False:
            icon = pg.transform.flip(icon, True, False)
        screen.blit(icon, (x, y))

    @staticmethod
    def render_timer(screen: pg.Surface, time_to_print: str):
        text = Text((WIDTH // 2, HEIGHT // 25.714),
                    time_to_print,
                    (WIDTH + HEIGHT) // 45,
                    SWAMP_COLOR)
        text.render(screen)

    def render_background(self, screen: pg.Surface):
        screen.blit(self.__background, (0, 0))

    @staticmethod
    def create_background() -> pg.Surface:
        path_to_background = 'view/sprites/Background.png'
        background_image = pg.image.load(path_to_background).convert_alpha()
        background_image = pg.transform.scale(background_image, (WIDTH, HEIGHT))
        return background_image

    @staticmethod
    def create_background_for_maze(backgrund_size: tuple[int, int]) -> pg.Surface:
        size = backgrund_size
        image = pg.Surface(size)
        image.fill(DEEP_GREEN_COLOR)
        return image

    @staticmethod
    def create_player_icon_in_maze() -> pg.Surface:
        path_to_capybara = 'view/sprites/capy_for_maze.png'
        capybara_image = pg.image.load(path_to_capybara).convert_alpha()
        return capybara_image

    @staticmethod
    def create_prize_icon() -> pg.Surface:
        path_to_prize = 'view/sprites/orange.png'
        prize_image = pg.image.load(path_to_prize).convert_alpha()
        return prize_image

