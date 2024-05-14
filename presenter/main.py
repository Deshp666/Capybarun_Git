from view.main import SceneRender
from view.constants import WIDTH, HEIGHT, FPS, CAPTION, MAZE_WIDTH, MAZE_HEIGHT, MAZE_INDENTATION_Y,\
    MAZE_INDENTATION_X
from view.buttons import Button
from model.main import Model
import pygame as pg
import sys
from enum import Enum
pg.init()


class SceneState(Enum):
    menu = 0
    game = 1
    maze = 2
    final = 3


class Presenter:
    def __init__(self):
        self.__screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(CAPTION)
        self.__clock = pg.time.Clock()
        self.__scene = SceneState.menu
        self.__game_logic = Model()
        self.__game_logic.prepare_data(MAZE_WIDTH,
                                       MAZE_HEIGHT,
                                       MAZE_INDENTATION_X,
                                       MAZE_INDENTATION_Y)
        self.__scene_render = SceneRender()
        self.__buttons: dict[str:Button] = self.__scene_render.get_buttons()

    def handle_event(self):
        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                sys.exit()

            elif event.type == pg.MOUSEBUTTONUP:
                if self.__scene == SceneState.menu:
                    self.handle_menu_click()

                elif self.__scene == SceneState.final:
                    self.handle_final_click()

        if self.__scene == SceneState.game:
            self.handle_game_click()

        if self.__scene == SceneState.maze:
            self.handle_maze_movement()

    def handle_menu_click(self):
        start_button = self.__buttons['start_button']
        x, y = pg.mouse.get_pos()
        if start_button.collide_click((x, y)):
            self.__scene = SceneState.game

    def handle_game_click(self):
        keys = pg.key.get_pressed()
        if not self.__game_logic.is_capybara_dead():
            if keys[pg.K_UP] or keys[pg.K_SPACE] or keys[pg.K_w]:
                self.__game_logic.run(True)
            else:
                self.__game_logic.run(False)
        else:
            self.__scene = SceneState.maze

    def handle_maze_movement(self):
        keys = pg.key.get_pressed()
        if self.__game_logic.is_maze_time_not_over() is True:
            self.__game_logic.player_in_maze_move(keys)
            if self.__game_logic.is_prize_received():
                self.__scene = SceneState.game
        elif self.__game_logic.is_maze_time_not_over() is False:
            self.__scene = SceneState.final

    def handle_final_click(self):
        pass

    def restart_game(self):
        pass

    def render(self):
        if self.__scene == SceneState.menu:
            self.__scene_render.render_menu_scene(self.__screen)

        elif self.__scene == SceneState.game:
            record = self.__game_logic.get_record_value()
            capybara_rect = self.__game_logic.get_capybara_rect()
            enemy_rect = self.__game_logic.get_enemy_information()
            pause_condition = self.__game_logic.get_pause_condition()
            self.__scene_render.render_game_scene(self.__screen,
                                                  record,
                                                  capybara_rect,
                                                  enemy_rect,
                                                  pause_condition)

        elif self.__scene == SceneState.maze:
            time_to_print = self.__game_logic.get_time_for_print()
            maze = self.__game_logic.get_maze_to_render()
            maze_size = self.__game_logic.get_maze_size()
            player_in_maze_rect = self.__game_logic.get_maze_player_rect()
            prize_rect = self.__game_logic.get_prize_rect()
            self.__scene_render.render_maze_scene(self.__screen,
                                                  time_to_print,
                                                  maze,
                                                  maze_size,
                                                  player_in_maze_rect,
                                                  prize_rect)

        elif self.__scene == SceneState.final:
            self.__scene_render.render_final_scene(self.__screen)

    def mainloop(self):
        while True:
            self.render()
            self.handle_event()

            self.__clock.tick(FPS)
