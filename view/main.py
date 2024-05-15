import pygame as pg
from view.constants import WHITE_COLOR, GRAY_COLOR, PEACH_COLOR, WIDTH, HEIGHT, SWAMP_COLOR, DEEP_GREEN_COLOR, \
    MAZE_HEIGHT, MAZE_WIDTH, CAPTION, TIMER_COORDINATES, TIMER_FONT_SIZE, RECORD_COORDINATES, RECORD_FONT_SIZE, \
    PAUSE_MENU_SIZE, PAUSE_FONT_SIZE, PAUSE_COORDINATES, CAPTION_TEXT_COORDINATES, CAPTION_TEXT_SIZE, \
    START_BUTTON_COORDINATES, START_BUTTON_SIZE, START_BUTTON_FONT_SIZE, BLACK_COLOR, MAZE_BACKGROUND_SIZE, HALF_WIDTH,\
    HALF_HEIGHT
from view.buttons import Button, Text
from view.paths import BG_FOR_TEXT_PATH, MUSIC_TURN_ON_BUTTON_PATH, MUSIC_TURN_OFF_BUTTON_PATH
from view.sprites import Sprites
pg.init()


class SceneRender:
    def __init__(self):
        self.__buttons = {
            'start_button': Button(START_BUTTON_COORDINATES,
                                   'START', START_BUTTON_SIZE,
                                   START_BUTTON_FONT_SIZE,
                                   BG_FOR_TEXT_PATH),
            'pause_button': Button(PAUSE_COORDINATES,
                                   'PAUSE',
                                   PAUSE_MENU_SIZE, PAUSE_FONT_SIZE, BG_FOR_TEXT_PATH)
        }
        self.__text = {
            'caption': Text(CAPTION_TEXT_COORDINATES,
                            CAPTION,
                            CAPTION_TEXT_SIZE)
        }
        self.__sprites = Sprites()
        self.__first_background_part_x = 0
        self.__second_background_part_x = WIDTH
        self.e = 0
        self.c = 0

    def render_menu_scene(self, screen: pg.Surface):
        self.render_background(screen)
        self.__buttons['start_button'].render(screen)
        self.__text['caption'].render(screen)
        pg.display.update()

    def render_background(self, screen: pg.Surface):
        background = pg.transform.scale(self.__sprites.background, (WIDTH, HEIGHT))
        screen.blit(background, (0, 0))

    def render_game_scene(self, screen: pg.Surface,
                          record: str,
                          capybara_information: tuple[pg.Rect, bool],
                          enemy_information: tuple[pg.Rect, str],
                          pause_state: bool):
        if pause_state:
            need_to_move_bg = False
        else:
            need_to_move_bg = True
        self.render_dynamic_background(screen, need_to_move_bg)
        self.render_capybara_icon(screen, capybara_information)
        self.render_enemy(screen, enemy_information)
        self.render_score(screen, record)
        if pause_state:
            self.render_pause(screen)
        pg.display.update()

    def render_dynamic_background(self, screen: pg.Surface, need_to_move: bool):
        first_bg_part = pg.transform.scale(self.__sprites.background, (WIDTH, HEIGHT))
        second_bg_part = pg.transform.scale(self.__sprites.background, (WIDTH, HEIGHT))
        if need_to_move:
            if self.__first_background_part_x <= -WIDTH:
                self.__first_background_part_x = WIDTH
            if self.__second_background_part_x <= -WIDTH:
                self.__second_background_part_x = WIDTH
            self.__first_background_part_x -= 2
            self.__second_background_part_x -= 2
        screen.blit(first_bg_part, (self.__first_background_part_x, 0))
        screen.blit(second_bg_part, (self.__second_background_part_x, 0))

    def render_capybara_icon(self, screen, capybara_information: tuple[pg.Rect, bool]):
        player_rect = capybara_information[0]
        is_on_ground = capybara_information[1]
        width = player_rect.width
        height = player_rect.height
        x = player_rect.x
        y = player_rect.y
        ind = int(self.c)
        animation_sprites = self.__sprites.capybara_animation
        jump_sprite = self.__sprites.capybara_jump
        if is_on_ground:
            sprite = pg.transform.scale(animation_sprites[ind], (width, height))
            screen.blit(sprite, (x, y))
            if self.c + 0.05 > 2:
                self.c = 0
            else:
                self.c += 0.05
        else:
            sprite = pg.transform.scale(jump_sprite, (width, height))
            screen.blit(sprite, (x, y))

    def render_enemy(self, screen: pg.Surface, enemy_information: tuple[pg.Rect, str] | None):
        if enemy_information is not None:
            enemy_rect = enemy_information[0]
            enemy_type = enemy_information[1]
            if enemy_type == 'bird':
                sprites = self.__sprites.bird_animation
            else:
                sprites = self.__sprites.bear_animation
            x = enemy_rect.x
            y = enemy_rect.y
            width = enemy_rect.width
            height = enemy_rect.height
            ind = sprites[int(self.e)]
            sprite = pg.transform.scale(ind, (width, height))
            screen.blit(sprite, (x, y))
            if self.e + 0.3 > 4:
                self.e = 0
            else:
                self.e += 0.3

            # sprites = pg.transform.scale(sprites, (width, height))
            # screen.blit(sprites, (x, y))

    @staticmethod
    def render_score(screen, record_to_print: str):
        record = Text(RECORD_COORDINATES,
                      record_to_print,
                      RECORD_FONT_SIZE,
                      SWAMP_COLOR)
        record.render(screen)

    def render_pause(self, screen):
        bg = pg.Surface((WIDTH, HEIGHT))
        bg.fill(BLACK_COLOR)
        bg.set_alpha(70)
        pause_button = self.__buttons['pause_button']
        screen.blit(bg, (0, 0))
        pause_button.render(screen)

    def render_maze_scene(self, screen: pg.Surface,
                          time_to_print: str,
                          maze_boundaries: list[pg.Rect],
                          maze_size: tuple[int, int],
                          player_in_maze_rect: tuple[pg.Rect, bool],
                          prize_rect: pg.Rect):
        self.render_dynamic_background(screen, False)
        self.render_maze(screen, maze_boundaries, maze_size)
        self.render_player_icon_maze(screen, player_in_maze_rect)
        self.render_prize(screen, prize_rect)
        self.render_timer(screen, time_to_print)
        pg.display.update()

    def render_maze(self, screen: pg.Surface, maze_boundaries: list[pg.Rect], maze_size: tuple[int, int]):
        background = self.create_background_for_maze(maze_size)
        screen.blit(background, MAZE_BACKGROUND_SIZE)
        for rect in maze_boundaries:
            pg.draw.rect(screen, PEACH_COLOR, rect)

    def render_player_icon_maze(self, screen: pg.Surface, player_in_maze_rect: tuple[pg.Rect, bool]):
        player_rect = player_in_maze_rect[0]
        looking_right = player_in_maze_rect[1]
        coordinates = player_rect.x, player_rect.y
        size = player_rect.width, player_rect.height
        icon = pg.transform.scale(self.__sprites.capybara_in_maze, size)
        if looking_right is False:
            icon = pg.transform.flip(icon, True, False)
        screen.blit(icon, coordinates)

    def render_prize(self, screen: pg.Surface, rect: pg.Rect):
        x = rect.x
        y = rect.y
        width = rect.width
        height = rect.height
        icon = pg.transform.scale(self.__sprites.prize, (width, height))
        screen.blit(icon, (x, y))

    @staticmethod
    def render_timer(screen: pg.Surface, time_to_print: str):
        timer = Text(TIMER_COORDINATES,
                     time_to_print,
                     TIMER_FONT_SIZE,
                     SWAMP_COLOR)
        timer.render(screen)

    def render_final_scene(self, screen: pg.Surface):
        self.render_background(screen)
        pg.display.update()

    @staticmethod
    def create_background_for_maze(background_size: tuple[int, int]) -> pg.Surface:
        size = background_size
        image = pg.Surface(size)
        image.fill(DEEP_GREEN_COLOR)
        return image

    @staticmethod
    def make_image(path: str) -> pg.Surface:
        image = pg.image.load(path).convert_alpha()
        return image

    def get_buttons(self) -> dict:
        return self.__buttons
