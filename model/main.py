import pygame as pg
from model.constants import DELTA_TIME, TIME_FOR_MAZE
from model.classes import Timer
from model.maze import Maze
pg.init()


class Model:
    def __init__(self):
        self.__speed = 1
        self.__record = 0
        self.__delta_time = 0
        self.__death_count = 1

    def update_death_count(self):
        self.__death_count += 1

    def create_timer(self) -> Timer:
        time = TIME_FOR_MAZE // self.__death_count
        timer = Timer(time)
        return timer

    def make_entity(self, x, y, width, height):
        pass

    def create_maze(self):
        maze = Maze()
        maze = maze.generate_maze()
        return maze
