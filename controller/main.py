from view.main import SceneRender
from view.constants import WIDTH, HEIGHT, FPS
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
        pg.display.set_caption('Capybarun')
        self.__clock = pg.time.Clock()
        self.__scene = SceneState.maze
        self.__game_logic = Model()
        self.__scene_render = SceneRender()
        self.__buttons: dict[str:Button] = self.__scene_render.get_buttons()

    def handle_event(self):
        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                sys.exit()

            elif event.type == pg.MOUSEBUTTONUP:
                x, y = event.pos
                if self.__scene == SceneState.menu:
                    self.handle_menu_click(x, y)

            elif event.type == pg.KEYDOWN:
                if self.__scene == SceneState.game:
                    self.handle_game_click()

                elif self.__scene == SceneState.maze:
                    self.handle_maze_movement()

    def handle_menu_click(self, x: int, y: int):
        start_button = self.__buttons['start_button']
        if start_button.collide_click((x, y)):
            self.__scene = SceneState.game

    def handle_game_click(self):
        pass

    def handle_maze_movement(self):
        pass

    def handle_final_click(self, x: int, y: int):
        pass

    def render(self):
        if self.__scene == SceneState.menu:
            self.__scene_render.render_menu_scene(self.__screen)

        elif self.__scene == SceneState.game:
            self.__scene_render.render_game_scene(self.__screen)

        elif self.__scene == SceneState.maze:
            time_to_print = '1'
            self.__scene_render.render_maze_scene(self.__screen, time_to_print)

        elif self.__scene == SceneState.final:
            self.__scene_render.render_final_scene(self.__screen)

    def mainloop(self):
        while True:
            self.handle_event()
            self.render()

            self.__clock.tick(FPS)
