import pygame as pg
from view.constants import WHITE_COLOR, GRAY_COLOR, PEACH_COLOR, WIDTH, HEIGHT, SWAMP_COLOR, DEEP_GREEN_COLOR, \
    MAZE_HEIGHT, MAZE_WIDTH, CAPTION, TIMER_COORDINATES, TIMER_FONT_SIZE, SCORE_COORDINATES, SCORE_FONT_SIZE, \
    PAUSE_MENU_SIZE, PAUSE_FONT_SIZE, PAUSE_COORDINATES, CAPTION_TEXT_COORDINATES, CAPTION_TEXT_SIZE, \
    START_BUTTON_COORDINATES, START_BUTTON_SIZE, START_BUTTON_FONT_SIZE, BLACK_COLOR, MAZE_BACKGROUND_COORDINATES, HALF_WIDTH,\
    HALF_HEIGHT, GAMEOVER_TEXT_COORDINATES, GAMEOVER_TEXT_FONT_SIZE, FINAL_SCREEN_BACKGROUND_SIZE, \
    FINAL_SCREEN_BACKGROUND_COORDINATES, SCORE_TEXT_COORDINATES, SCORE_NUM_TEXT_COORDINATES, RECORD_TEXT_COORDINATES, \
    RECORD_NUM__TEXT_COORDINATES, RESTART_BUTTON_FONT_SIZE, RESTART_BUTTON_COORDINATES, RESTART_BUTTON_SIZE, \
    FINAL_TEXT_FONT_SIZE, BACKGROUND_SPEED_MULTIPLIER, CAPYBARA_SPEED_MULTIPLIER, ENEMY_SPEED_MULTIPLIER
from view.buttons import Button, Text
from view.paths import BG_FOR_TEXT_PATH, MUSIC_TURN_ON_BUTTON_PATH, MUSIC_TURN_OFF_BUTTON_PATH
from view.sprites import Sprites
pg.init()


class SceneRender:
    def __init__(self):
        self.__buttons: dict[str: Button] = {
            'start_button': Button(START_BUTTON_COORDINATES,
                                   'START', START_BUTTON_SIZE,
                                   START_BUTTON_FONT_SIZE,
                                   BG_FOR_TEXT_PATH),

            'pause_button': Button(PAUSE_COORDINATES,
                                   'PAUSE',
                                   PAUSE_MENU_SIZE, PAUSE_FONT_SIZE,
                                   BG_FOR_TEXT_PATH),

            'restart_button': Button(RESTART_BUTTON_COORDINATES,
                                     'RESTART',
                                     RESTART_BUTTON_SIZE,
                                     RESTART_BUTTON_FONT_SIZE,
                                     BG_FOR_TEXT_PATH)
        }
        self.__text: dict[str: Button] = {
            'caption': Text(CAPTION_TEXT_COORDINATES,
                            CAPTION,
                            CAPTION_TEXT_SIZE),

            'score': Text(SCORE_TEXT_COORDINATES,
                          'SCORE',
                          FINAL_TEXT_FONT_SIZE),

            'record': Text(RECORD_TEXT_COORDINATES,
                           'RECORD',
                           FINAL_TEXT_FONT_SIZE),

            'gameover': Text(GAMEOVER_TEXT_COORDINATES,
                             'GAMEOVER',
                             GAMEOVER_TEXT_FONT_SIZE)
        }
        self.__sprites: Sprites = Sprites()
        self.__first_background_part_x: float = 0
        self.__first_background_part_y: float = 0
        self.__second_background_part_x: float = WIDTH
        self.__second_background_part_y: float = 0
        self.enemy_parameter_to_calculate_frame: float = 0
        self.capybara_parameter_to_calculate_frame: float = 0

    def render_menu_scene(self, screen: pg.Surface):
        self.render_background(screen)
        self.__buttons['start_button'].render(screen)
        self.__text['caption'].render(screen)
        pg.display.update()

    def render_background(self, screen: pg.Surface):
        size = WIDTH, HEIGHT
        coordinates = 0, 0
        background = pg.transform.scale(self.__sprites.background, size)
        screen.blit(background, coordinates)

    def render_runner_scene(self, screen: pg.Surface,
                            record: str,
                            capybara_information: tuple[pg.Rect, bool],
                            enemy_information: tuple[pg.Rect, str],
                            pause_state: bool,
                            speed: int):
        if pause_state or not capybara_information[1]:
            need_to_move_bg = False
        else:
            need_to_move_bg = True

        if pause_state:
            need_to_move_entity = False
        else:
            need_to_move_entity = True

        self.render_dynamic_background(screen, need_to_move_bg, speed)
        self.render_capybara_icon(screen, capybara_information, speed, need_to_move_entity)
        self.render_enemy(screen, enemy_information, speed, need_to_move_entity)
        self.render_score(screen, record)

        if pause_state:
            self.render_pause(screen)

        pg.display.update()

    def render_dynamic_background(self,
                                  screen: pg.Surface,
                                  need_to_move: bool,
                                  speed: int = 0):
        first_bg_part = pg.transform.scale(self.__sprites.background, (WIDTH, HEIGHT))
        second_bg_part = pg.transform.scale(self.__sprites.background, (WIDTH, HEIGHT))
        speed = speed / BACKGROUND_SPEED_MULTIPLIER

        if need_to_move:
            if self.__first_background_part_x <= -WIDTH:
                self.__first_background_part_x = WIDTH

            if self.__second_background_part_x <= -WIDTH:
                self.__second_background_part_x = WIDTH

            self.__first_background_part_x -= speed
            self.__second_background_part_x -= speed

        coordinates_for_first_part = self.__first_background_part_x, self.__first_background_part_y
        coordinates_for_second_part = self.__second_background_part_x, self.__second_background_part_y
        screen.blit(first_bg_part, coordinates_for_first_part)
        screen.blit(second_bg_part, coordinates_for_second_part)

    def render_capybara_icon(self,
                             screen: pg.Surface,
                             capybara_information: tuple[pg.Rect, bool],
                             speed: int,
                             need_to_move: bool):
        capybara_rect = capybara_information[0]
        is_capybara_on_ground = capybara_information[1]
        coordinates = capybara_rect.x, capybara_rect.y
        size = capybara_rect.width, capybara_rect.height
        speed = speed / CAPYBARA_SPEED_MULTIPLIER

        animations_frames = self.__sprites.capybara_animation
        animations_frames_count = len(animations_frames)
        jump_sprite = self.__sprites.capybara_jump
        frame_to_render = int(self.capybara_parameter_to_calculate_frame % animations_frames_count)

        if is_capybara_on_ground:
            frame = pg.transform.scale(animations_frames[frame_to_render], size)
            screen.blit(frame, coordinates)
            if need_to_move:
                self.capybara_parameter_to_calculate_frame += speed
        else:
            sprite = pg.transform.scale(jump_sprite, size)
            screen.blit(sprite, coordinates)

    def render_enemy(self,
                     screen: pg.Surface,
                     enemy_information: tuple[pg.Rect, str] | None,
                     speed: int,
                     need_to_move: bool):
        if enemy_information is not None:
            enemy_rect = enemy_information[0]
            coordinates = enemy_rect.x, enemy_rect.y
            size = enemy_rect.width, enemy_rect.height

            enemy_type = enemy_information[1]
            if enemy_type == 'bird':
                animations_frames = self.__sprites.bird_animation
            else:
                animations_frames = self.__sprites.bear_animation
            frames_count = len(animations_frames)
            frame_to_render = int(self.enemy_parameter_to_calculate_frame % frames_count)
            sprite = pg.transform.scale(animations_frames[frame_to_render], size)

            speed = speed / ENEMY_SPEED_MULTIPLIER
            screen.blit(sprite, coordinates)

            if need_to_move:
                self.enemy_parameter_to_calculate_frame += speed

    @staticmethod
    def render_score(screen: pg.Surface,
                     record_to_print: str):
        score = Text(SCORE_COORDINATES,
                     record_to_print,
                     SCORE_FONT_SIZE,
                     SWAMP_COLOR)
        score.render(screen)

    def render_pause(self, screen: pg.Surface):
        size = WIDTH, HEIGHT
        coordinates = 0, 0
        visibility_percent = 70

        background = pg.Surface(size)
        background.fill(BLACK_COLOR)
        background.set_alpha(visibility_percent)
        screen.blit(background, coordinates)

        pause_button = self.__buttons['pause_button']
        pause_button.render(screen)

    def render_maze_scene(self,
                          screen: pg.Surface,
                          time_to_print: str,
                          maze_boundaries: list[pg.Rect],
                          maze_size: tuple[int, int],
                          capybara_in_maze_information: tuple[pg.Rect, bool],
                          prize_rect: pg.Rect):
        self.render_dynamic_background(screen, need_to_move=False)
        self.render_maze(screen, maze_boundaries, maze_size)
        self.render_player_icon_maze(screen, capybara_in_maze_information)
        self.render_prize(screen, prize_rect)
        self.render_timer(screen, time_to_print)
        pg.display.update()

    def render_maze(self,
                    screen: pg.Surface,
                    maze_boundaries: list[pg.Rect],
                    maze_size: tuple[int, int]):
        background = self.create_background_for_maze(maze_size)
        screen.blit(background, MAZE_BACKGROUND_COORDINATES)
        for rect in maze_boundaries:
            pg.draw.rect(screen, PEACH_COLOR, rect)

    def render_player_icon_maze(self,
                                screen: pg.Surface,
                                capybara_in_maze_information: tuple[pg.Rect, bool]):
        capybara_rect = capybara_in_maze_information[0]
        coordinates = capybara_rect.x, capybara_rect.y
        size = capybara_rect.width, capybara_rect.height
        player_icon = pg.transform.scale(self.__sprites.capybara_in_maze, size)

        is_looking_right = capybara_in_maze_information[1]
        if is_looking_right is False:
            player_icon = pg.transform.flip(player_icon, True, False)
        screen.blit(player_icon, coordinates)

    def render_prize(self, screen: pg.Surface,
                     prize_rect: pg.Rect):
        coordinates = prize_rect.x, prize_rect.y
        size = prize_rect.width, prize_rect.height
        prize_icon = pg.transform.scale(self.__sprites.prize, size)
        screen.blit(prize_icon, coordinates)

    @staticmethod
    def render_timer(screen: pg.Surface,
                     time_to_print: str):
        timer = Text(TIMER_COORDINATES,
                     time_to_print,
                     TIMER_FONT_SIZE,
                     SWAMP_COLOR)
        timer.render(screen)

    def render_final_scene(self,
                           screen: pg.Surface,
                           score: str,
                           record: str):
        self.render_background(screen)
        self.render_final_screen(screen, score, record)
        pg.display.update()

    def render_final_screen(self, screen: pg.Surface, score: str, record: str):
        bg_image = self.__sprites.bg_final
        bg_image = pg.transform.scale(bg_image, FINAL_SCREEN_BACKGROUND_SIZE)
        screen.blit(bg_image, FINAL_SCREEN_BACKGROUND_COORDINATES)

        score_num = Text(SCORE_NUM_TEXT_COORDINATES, score, FINAL_TEXT_FONT_SIZE, WHITE_COLOR)
        record_num = Text(RECORD_NUM__TEXT_COORDINATES, record, FINAL_TEXT_FONT_SIZE, WHITE_COLOR)
        score_num.render(screen)
        record_num.render(screen)
        self.__text['gameover'].render(screen)
        self.__text['score'].render(screen)
        self.__text['record'].render(screen)
        self.__buttons['restart_button'].render(screen)

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

    def get_buttons(self) -> dict[str: Button]:
        return self.__buttons
