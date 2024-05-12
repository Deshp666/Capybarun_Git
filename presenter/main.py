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
        self.__scene = SceneState.maze
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
        pass

    def handle_maze_movement(self):
        keys = pg.key.get_pressed()
        if self.__game_logic.is_maze_time_not_over() is True:
            if keys[pg.K_SPACE]:
                pass
        elif self.__game_logic.is_maze_time_not_over() is False:
            self.__scene = SceneState.final
            # self.__player_in_maze.move_right()

    def handle_final_click(self):
        pass

    def restart_game(self):
        pass

    def render(self):
        if self.__scene == SceneState.menu:
            self.__scene_render.render_menu_scene(self.__screen)

        elif self.__scene == SceneState.game:
            self.__scene_render.render_game_scene(self.__screen)

        elif self.__scene == SceneState.maze:
            time_to_print = self.__game_logic.get_time_for_print()
            maze = self.__game_logic.get_maze_to_render()
            maze_size = self.__game_logic.get_maze_size()
            self.__scene_render.render_maze_scene(self.__screen,
                                                  time_to_print,
                                                  maze,
                                                  maze_size)

        elif self.__scene == SceneState.final:
            self.__scene_render.render_final_scene(self.__screen)

    def mainloop(self):
        while True:
            self.render()
            self.handle_event()

            self.__clock.tick(FPS)
