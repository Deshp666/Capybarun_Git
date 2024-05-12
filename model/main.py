import pygame as pg
from model.constants import DELTA_TIME, TIME_FOR_MAZE, CELL_SIZE
from model.classes import Timer, Record
from model.maze import Maze, MazePlayer
pg.init()


class Model:
    def __init__(self):
        self.__speed: int = 1
        self.__death_count: int = 1
        self.__timers_list: list[Timer] = []
        self.__mazes_list: list[Maze] = []
        self.__record: Record = Record()

    def prepare_data(self, maze_width: int,
                     maze_height: int,
                     indentation_x: int,
                     indentation_y: int):
        for death in range(1, 5):
            cell_size = CELL_SIZE // death
            self.__mazes_list.append(Maze(cell_size,
                                          maze_width,
                                          maze_height,
                                          indentation_x,
                                          indentation_y))
            time = TIME_FOR_MAZE // death
            self.__timers_list.append(Timer(time))

    def is_maze_time_not_over(self) -> bool:
        return self.__timers_list[self.__death_count].update()

    def get_time_for_print(self):
        return self.__timers_list[self.__death_count].get_for_print()

    def get_maze_to_render(self):
        maze = self.__mazes_list[self.__death_count]
        rects = []
        cells_list = maze.get_cells_grid()
        for cell in cells_list:
            rects += cell.get_boundaries()
        return rects

    def get_maze_size(self):
        maze = self.__mazes_list[self.__death_count]
        return maze.get_size()

    def update_death_count(self):
        self.__death_count += 1

    def make_entity(self, x, y, width, height):
        pass

    def create_player_for_maze(self) -> MazePlayer:
        pass
