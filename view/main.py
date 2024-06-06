import pygame as pg
from view.constants import *
from view.interface_elements import *
from view.paths import *
from view.sprites import *
from abc import abstractmethod


class StartRender:
    def __init__(self):
        self.__start_screen_buttons = StartSceneButtons
        self.__sound_buttons = SoundButtons
        self.__texts = StartSceneTexts
        self.__sprites = StartSceneSprites()

    def render_scene(self, screen: pg.Surface, sounds_on: bool):
        render_background(screen)

        start_button = self.__start_screen_buttons.start_button
        turn_on_button = self.__sound_buttons.turn_on_sound
        turn_off_button = self.__sound_buttons.turn_off_sound
        caption_text = self.__texts.caption

        start_button.render(screen)

        if sounds_on:
            turn_on_button.render(screen)
        else:
            turn_off_button.render(screen)

        caption_text.render(screen)

        pg.display.update()

    def __render_background(self, screen: pg.Surface):
        size = SCREEN_WIDTH, SCREEN_HEIGHT
        coordinates = 0, 0
        background = pg.transform.scale(self.__sprites.background, size)
        screen.blit(background, coordinates)


class RunnerRender:
    def __init__(self):
        self.__sound_buttons = SoundButtons
        self.__sprites = RunnerSceneSprites()
        self.__first_background_part_x: float = 0
        self.__first_background_part_y: float = 0
        self.__second_background_part_x: float = SCREEN_WIDTH
        self.__second_background_part_y: float = 0
        self.__enemy_parameter_to_calculate_frame: float = 0
        self.__capybara_parameter_to_calculate_frame: float = 0

    def render_scene(self,
                     screen: pg.Surface,
                     record: str,
                     capybara_information: tuple[pg.Rect, bool],
                     enemy_information: tuple[pg.Rect, str],
                     pause_state: bool,
                     speed: int,
                     sound_state: bool):
        if pause_state or not capybara_information[1]:
            need_to_move_bg = False
        else:
            need_to_move_bg = True

        if pause_state:
            need_to_move_entity = False
        else:
            need_to_move_entity = True

        self.__render_dynamic_background(screen, need_to_move_bg, speed)
        self.__render_capybara_icon(screen, capybara_information, speed, need_to_move_entity)
        self.__render_enemy(screen, enemy_information, speed, need_to_move_entity)
        self.__render_score(screen, record)

        if pause_state:
            self.__render_pause(screen, sound_state)

        pg.display.update()

    def __render_dynamic_background(self,
                                    screen: pg.Surface,
                                    need_to_move: bool,
                                    speed: int = 0):
        first_bg_part = pg.transform.scale(self.__sprites.first_background_part, (SCREEN_WIDTH, SCREEN_HEIGHT))
        second_bg_part = pg.transform.scale(self.__sprites.second_background_part, (SCREEN_WIDTH, SCREEN_HEIGHT))
        animation_speed = speed / BACKGROUND_SPEED_MULTIPLIER

        if need_to_move:
            if self.__first_background_part_x <= -SCREEN_WIDTH:
                self.__first_background_part_x = SCREEN_WIDTH

            if self.__second_background_part_x <= -SCREEN_WIDTH:
                self.__second_background_part_x = SCREEN_WIDTH

            self.__first_background_part_x -= animation_speed
            self.__second_background_part_x -= animation_speed

        coordinates_for_first_part = self.__first_background_part_x, self.__first_background_part_y
        coordinates_for_second_part = self.__second_background_part_x, self.__second_background_part_y
        screen.blit(first_bg_part, coordinates_for_first_part)
        screen.blit(second_bg_part, coordinates_for_second_part)

    def __render_capybara_icon(self,
                               screen: pg.Surface,
                               capybara_information: tuple[pg.Rect, bool],
                               speed: int,
                               need_to_move: bool):
        capybara_rect = capybara_information[0]
        is_capybara_on_ground = capybara_information[1]
        coordinates = capybara_rect.x, capybara_rect.y
        size = capybara_rect.width, capybara_rect.height
        animation_speed = speed / CAPYBARA_SPEED_MULTIPLIER

        animations_frames = self.__sprites.capybara_animation
        animations_frames_count = len(animations_frames)
        jump_sprite = self.__sprites.capybara_jump
        frame_to_render = int(self.__capybara_parameter_to_calculate_frame % animations_frames_count)

        if is_capybara_on_ground:
            frame = pg.transform.scale(animations_frames[frame_to_render], size)
            screen.blit(frame, coordinates)
            if need_to_move:
                self.__capybara_parameter_to_calculate_frame += animation_speed
        else:
            sprite = pg.transform.scale(jump_sprite, size)
            screen.blit(sprite, coordinates)

    def __render_enemy(self,
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
            frame_to_render = int(self.__enemy_parameter_to_calculate_frame % frames_count)
            sprite = pg.transform.scale(animations_frames[frame_to_render], size)

            animation_speed = speed / ENEMY_SPEED_MULTIPLIER
            screen.blit(sprite, coordinates)

            if need_to_move:
                self.__enemy_parameter_to_calculate_frame += animation_speed

    @staticmethod
    def __render_score(screen: pg.Surface,
                       record_to_print: str):
        score = Text(SCORE_COORDINATES,
                     record_to_print,
                     SCORE_FONT_SIZE,
                     SWAMP_COLOR)
        score.render(screen)

    def __render_pause(self, screen: pg.Surface, sound_state: bool):
        size = SCREEN_WIDTH, SCREEN_HEIGHT
        coordinates = 0, 0
        visibility_percent = 70

        background = pg.Surface(size)
        background.fill(BLACK_COLOR)
        background.set_alpha(visibility_percent)
        screen.blit(background, coordinates)

        pause_button = self.__buttons.pause_button
        turn_on_button = self.__buttons.turn_on_sound
        turn_off_button = self.__buttons.turn_off_sound

        if sound_state:
            turn_on_button.render(screen)
        else:
            turn_off_button.render(screen)

        pause_button.render(screen)


class MazeRender:
    def __init__(self):
        self.__sprites = MazeSceneSprites()

    def render_scene(self,
                     screen: pg.Surface,
                     time_to_print: str,
                     maze_boundaries: list[pg.Rect],
                     maze_size: tuple[int, int],
                     capybara_in_maze_information: tuple[pg.Rect, bool],
                     prize_rect: pg.Rect):
        render_background(screen)
        self.__render_maze(screen, maze_boundaries, maze_size)
        self.__render_player_icon_maze(screen, capybara_in_maze_information)
        self.__render_prize(screen, prize_rect)
        self.__render_timer(screen, time_to_print)
        pg.display.update()

    def __render_maze(self,
                      screen: pg.Surface,
                      maze_boundaries: list[pg.Rect],
                      maze_size: tuple[int, int]):
        background = self.__create_background_for_maze(maze_size)
        screen.blit(background, MAZE_BACKGROUND_COORDINATES)
        for rect in maze_boundaries:
            pg.draw.rect(screen, PEACH_COLOR, rect)

    def __render_player_icon_maze(self,
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

    def __render_prize(self, screen: pg.Surface,
                       prize_rect: pg.Rect):
        coordinates = prize_rect.x, prize_rect.y
        size = prize_rect.width, prize_rect.height
        prize_icon = pg.transform.scale(self.__sprites.prize, size)
        screen.blit(prize_icon, coordinates)

    @staticmethod
    def __render_timer(screen: pg.Surface,
                       time_to_print: str):
        timer = Text(TIMER_COORDINATES,
                     time_to_print,
                     TIMER_FONT_SIZE,
                     SWAMP_COLOR)
        timer.render(screen)

    @staticmethod
    def __create_background_for_maze(background_size: tuple[int, int]) -> pg.Surface:
        size = background_size
        image = pg.Surface(size)
        image.fill(DEEP_GREEN_COLOR)
        return image


class FinalRender:
    def __init__(self):
        self.__sprites = FinalSceneSprites()
        self.__texts = FinalSceneTexts
        self.__buttons = FinalSceneButtons

    def render_scene(self, screen: pg.Surface, score: str, record: str):
        render_background(screen)
        self.__render_final_screen(screen, score, record)
        pg.display.update()

    def __render_final_screen(self, screen: pg.Surface, score: str, record: str):
        bg_image = self.__sprites.bg_menu_final
        bg_image = pg.transform.scale(bg_image, FINAL_SCREEN_BACKGROUND_SIZE)
        screen.blit(bg_image, FINAL_SCREEN_BACKGROUND_COORDINATES)

        score_num = Text(SCORE_NUM_TEXT_COORDINATES, score, FINAL_TEXT_FONT_SIZE, WHITE_COLOR)
        record_num = Text(RECORD_NUM__TEXT_COORDINATES, record, FINAL_TEXT_FONT_SIZE, WHITE_COLOR)
        gameover_text = self.__texts.gameover
        score_text = self.__texts.gameover
        record_text = self.__texts.record
        restart_button = self.__buttons.restart_button

        score_num.render(screen)
        record_num.render(screen)
        gameover_text.render(screen)
        score_text.render(screen)
        record_text.render(screen)
        restart_button.render(screen)


class ViewController:
    def __init__(self):
        self.__text: TextsCollection = TextsCollection()
        self.__buttons: InterfaceButtons = InterfaceButtons()
        self.__sprites: Sprites = Sprites()
        self.__start_scene_render = StartRender()
        self.__runner_scene_render = RunnerRender()
        self.__maze_scene_render = MazeRender()
        self.__final_scene_render = FinalRender()

    def render_start_scene(self, screen: pg.Surface, sounds_on: bool):
        self.__start_scene_render.render_scene(screen, sounds_on)

    def render_runner_scene(self, screen: pg.Surface,
                            record: str,
                            capybara_information: tuple[pg.Rect, bool],
                            enemy_information: tuple[pg.Rect, str],
                            pause_state: bool,
                            speed: int,
                            sound_state: bool):
        self.__runner_scene_render.render_scene(screen,
                                                record,
                                                capybara_information,
                                                enemy_information,
                                                pause_state,
                                                speed,
                                                sound_state)

    def render_maze_scene(self,
                          screen: pg.Surface,
                          time_to_print: str,
                          maze_boundaries: list[pg.Rect],
                          maze_size: tuple[int, int],
                          capybara_in_maze_information: tuple[pg.Rect, bool],
                          prize_rect: pg.Rect):
        self.__maze_scene_render.render_scene(screen,
                                              time_to_print,
                                              maze_boundaries,
                                              maze_size,
                                              capybara_in_maze_information,
                                              prize_rect)

    def render_final_scene(self,
                           screen: pg.Surface,
                           score: str,
                           record: str):
        self.__final_scene_render.render_scene(screen, score, record)

    def get_buttons(self) -> InterfaceButtons:
        return self.__buttons


def render_background(screen: pg.Surface):
    size = SCREEN_WIDTH, SCREEN_HEIGHT
    coordinates = 0, 0
    background = create_background()
    background = pg.transform.scale(background, size)
    screen.blit(background, coordinates)
