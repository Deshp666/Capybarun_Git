import sys
import pygame as pg
import time
pg.init()


class Timer:
    def __init__(self, time: int):
        self.time = time

    def get_time(self, for_loop = False):
        minutes = self.time // 60
        seconds = self.time % 60
        if for_loop:
            return self.time
        else:
            return minutes, seconds

    def update_time(self):
        while self.time > 0:
            self.time -= 1

    def get_time_to_print(self):
        minutes, seconds = self.get_time()
        if seconds < 10:
            seconds = '0' + str(seconds)
        str_time = f'0{minutes}:{seconds}'
        return str_time


class Entity:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = self.make_hitbox()

    def make_hitbox(self) -> pg.Rect:
        rect = pg.Rect(self.x, self.y, self.width, self.height)
        return rect

    def get_hitbox(self):
        return self.hitbox

    def move_right(self):
        self.hitbox.x += 0.5

    def get_coordinates(self):
        return self.x, self.y


class Model:
    def __init__(self):
        self.__speed = 1
        self.__record = 0
        self.__time = 0
        self.__death_count = 1

    def update_death_count(self):
        self.__death_count += 1

    def create_timer(self) -> Timer:
        time = 60 // self.__death_count
        timer = Timer(time)
        return timer

    def make_entity(self, x, y, width, height):
        entity = Entity(x, y, width, height)
        return entity

# timer = Timer(5)
# while True:
#     print(timer.get_time_to_print())
#     timer.update_time()
#     if timer.get_time(True) == 0:
#         print(timer.get_time_to_print())
#         break
