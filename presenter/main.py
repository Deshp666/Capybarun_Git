from view.main import SceneRender
from view.constants import WIDTH, HEIGHT, FPS, CAPTION, MAZE_WIDTH, MAZE_HEIGHT, MAZE_INDENTATION_Y, \
    MAZE_INDENTATION_X
from view.buttons import Button
from model.main import Model
import pygame as pg
import sys
from enum import Enum

pg.init()


class SceneState(Enum):
    menu = 0
    runner = 1
    maze = 2
    final = 3


class Presenter:
    def __init__(self):
        self.__screen: pg.Surface = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(CAPTION)
        self.__scene: Enum = SceneState.menu
        self.__clock: pg.time.Clock = pg.time.Clock()
        self.__game_logic: Model = Model(MAZE_WIDTH,
                                         MAZE_HEIGHT,
                                         MAZE_INDENTATION_X,
                                         MAZE_INDENTATION_Y)
        self.__scene_render: SceneRender = SceneRender()
        self.__buttons: dict[str:Button] = self.__scene_render.get_buttons()

    def handle_event(self):
        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                self.__game_logic.save_record()
                sys.exit()

            if event.type == pg.MOUSEBUTTONUP or event.type == pg.KEYDOWN:
                if self.__scene == SceneState.menu:
                    self.handle_menu_click()

                elif self.__scene == SceneState.final:
                    self.handle_final_click()

                elif self.__game_logic.get_pause_condition():
                    self.handle_pause_click()

            if event.type == pg.KEYDOWN and SceneState.runner:
                if event.key == pg.K_ESCAPE:
                    self.__game_logic.toggle_pause()

        if self.__scene == SceneState.runner:
            self.handle_runner_click()

        if self.__scene == SceneState.maze:
            self.handle_maze_movement()

    def handle_menu_click(self):
        keys = pg.key.get_pressed()
        start_button = self.__buttons['start_button']
        x, y = pg.mouse.get_pos()
        if start_button.collide_click((x, y)) or keys[pg.K_RETURN]:
            self.__scene = SceneState.runner

    def handle_runner_click(self):
        keys = pg.key.get_pressed()
        if not self.__game_logic.is_capybara_dead():
            if keys[pg.K_UP] or keys[pg.K_SPACE] or keys[pg.K_w]:
                self.__game_logic.run(True)
            elif keys[pg.K_DOWN] or keys[pg.K_s]:
                self.__game_logic.run(False, True)
            else:
                self.__game_logic.run(False)
        else:
            self.__scene = SceneState.maze

    def handle_pause_click(self):
        pause_button = self.__buttons['pause_button']
        x, y = pg.mouse.get_pos()
        if pause_button.collide_click((x, y)):
            self.__game_logic.toggle_pause()

    def handle_maze_movement(self):
        keys = pg.key.get_pressed()
        if self.__game_logic.is_maze_time_not_over() is True:
            self.__game_logic.capybara_in_maze_move(keys)

            if self.__game_logic.is_prize_received():
                if self.__game_logic.get_pause_condition():
                    self.__game_logic.toggle_pause()
                self.__scene = SceneState.runner

        elif self.__game_logic.is_maze_time_not_over() is False:
            self.__game_logic.save_record()
            self.__scene = SceneState.final

    def handle_final_click(self):
        keys = pg.key.get_pressed()
        restart_button = self.__buttons['restart_button']
        x, y = pg.mouse.get_pos()
        if restart_button.collide_click((x, y)) or keys[pg.K_RETURN]:
            self.restart_game()

    def restart_game(self):
        self.__scene = SceneState.runner
        self.__game_logic = Model(MAZE_WIDTH,
                                  MAZE_HEIGHT,
                                  MAZE_INDENTATION_X,
                                  MAZE_INDENTATION_Y)
        self.__scene_render = SceneRender()

    def render(self):
        if self.__scene == SceneState.menu:
            self.render_menu_scene()

        elif self.__scene == SceneState.runner:
            self.render_runner_scene()

        elif self.__scene == SceneState.maze:
            self.render_maze_scene()

        elif self.__scene == SceneState.final:
            self.render_final_scene()

    def render_menu_scene(self):
        self.__scene_render.render_menu_scene(self.__screen)

    def render_runner_scene(self):
        record = self.__game_logic.get_record_value()
        capybara_rect = self.__game_logic.get_capybara_rect()
        is_capybara_jump = self.__game_logic.get_capybara_state()
        enemy_rect = self.__game_logic.get_enemy_information()
        pause_condition = self.__game_logic.get_pause_condition()
        speed = self.__game_logic.get_capybara_speed()
        self.__scene_render.render_runner_scene(self.__screen,
                                                record,
                                                (capybara_rect, is_capybara_jump),
                                                enemy_rect,
                                                pause_condition,
                                                speed)

    def render_maze_scene(self):
        time_to_print = self.__game_logic.get_time_for_print()
        maze = self.__game_logic.get_maze_to_render()
        maze_size = self.__game_logic.get_maze_size()
        capybara_in_maze_information = self.__game_logic.get_maze_capybara_information()
        prize_rect = self.__game_logic.get_prize_rect()
        self.__scene_render.render_maze_scene(self.__screen,
                                              time_to_print,
                                              maze,
                                              maze_size,
                                              capybara_in_maze_information,
                                              prize_rect)

    def render_final_scene(self):
        score = self.__game_logic.get_score()
        record = self.__game_logic.get_record()
        self.__scene_render.render_final_scene(self.__screen, score, record)

    def mainloop(self):
        while True:
            self.render()
            self.handle_event()

            self.__clock.tick(FPS)
