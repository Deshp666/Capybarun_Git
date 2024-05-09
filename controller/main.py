from view.main import SceneRender
from view.constants import WIDTH, HEIGHT, FPS, CAPTION
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


class Controller:
    def __init__(self):
        self.__screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(CAPTION)
        self.__clock = pg.time.Clock()
        self.__scene = SceneState.maze
        self.__game_logic = Model()
        self.__scene_render = SceneRender()
        # self.__player_in_maze = self.__game_logic.make_entity(100, 100, 50, 50)
        self.__buttons: dict[str:Button] = self.__scene_render.get_buttons()
        self.timer = self.__game_logic.create_timer()  # сделать инициализацию не тут, если здесь рандома не будет.
        self.maze = self.__game_logic.create_maze()

    def handle_event(self):
        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                sys.exit()

            elif event.type == pg.MOUSEBUTTONUP:
                if self.__scene == SceneState.menu:
                    self.handle_menu_click()

        if self.__scene == SceneState.game:
            self.handle_game_click()

        if self.__scene == SceneState.maze:
            self.handle_maze_movement()

        if self.__scene == SceneState.final:
            self.handle_final_click()

    def handle_menu_click(self):
        start_button = self.__buttons['start_button']
        x, y = pg.mouse.get_pos()
        if start_button.collide_click((x, y)):
            self.__scene = SceneState.game

    def handle_game_click(self):
        pass

    def handle_maze_movement(self):
        keys = pg.key.get_pressed()
        if self.timer.update() is True:
            if keys[pg.K_SPACE]:
                pass
        elif self.timer.update() is False:
            self.__scene = SceneState.final
            # self.__player_in_maze.move_right()

    def handle_final_click(self):
        pass

    def render(self):
        if self.__scene == SceneState.menu:
            self.__scene_render.render_menu_scene(self.__screen)

        elif self.__scene == SceneState.game:
            self.__scene_render.render_game_scene(self.__screen)

        elif self.__scene == SceneState.maze:
            time_to_print = self.timer.get_for_print()
            maze = self.make_maze_to_render()
            self.__scene_render.render_maze_scene(self.__screen,
                                                  time_to_print, maze)

        elif self.__scene == SceneState.final:
            self.__scene_render.render_final_scene(self.__screen)

    def make_maze_to_render(self):
        rects = []
        for cell in self.maze:
            rects += cell.get_boundaries()
        return rects

    def mainloop(self):
        while True:
            self.render()
            self.handle_event()

            self.__clock.tick(FPS)
