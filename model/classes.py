import random
from abc import ABC, abstractmethod
from model.constants import DELTA_TIME, GRAVITY, CAPYBARA_BASE_SPEED, CAPYBARA_JUMP_SPEED, CAPYBARA_BONUS_SPEED, \
    CAPYBARA_JUMP_HEIGHT
from presenter.constants import CAPYBARA_WIDTH, CAPYBARA_HEIGHT, CAPYBARA_POS_X, CAPYBARA_Y_POS, BEAR_POS_Y, ENEMY_START_POS_X,\
    BIRD_CENTER_POS_Y, BIRD_TOP_POS_Y, GROUND_HEIGHT, BIRD_HEIGHT, BEAR_HEIGHT, BIRD_WIDTH, BEAR_WIDTH, GROUND_Y_POS
import pickle
import pygame as pg
from random import randint
pg.init()


class TimeDependent(ABC):
    @abstractmethod
    def get_for_print(self) -> str:
        pass

    @abstractmethod
    def update(self):
        pass


class Timer(TimeDependent):
    def __init__(self, time: int):
        self.__value = time

    def update(self) -> bool:
        if self.__value > 0:
            self.__value -= DELTA_TIME
            return True
        elif self.__value - DELTA_TIME < 0:
            return False

    def get_for_print(self) -> str:
        minutes, seconds = self.get_time()
        if seconds < 10:
            seconds = '0' + str(seconds)
        str_time = f'0{minutes}:{seconds}'
        return str_time

    def get_time(self) -> tuple[int, int]:
        time = round(self.__value)
        minutes = time // 60
        seconds = time % 60
        return minutes, seconds


class Record(TimeDependent):
    def __init__(self):
        self.value = 0

    def update(self):
        self.value += DELTA_TIME

    def get_for_print(self) -> str:
        record = self.get_record()
        record_to_print = ''

        if record < 10:
            record_to_print = f'000{record_to_print}'
        elif 10 < record < 100:
            record_to_print = f'00{record_to_print}'
        elif 100 < record < 1000:
            record_to_print = f'0{record_to_print}'
        else:
            record_to_print = str(record_to_print)

        return record_to_print

    def get_record(self) -> int:
        return round(self.value)

    def save(self):
        with open('record.pickle', 'wb') as file:
            pickle.dump(self.get_record(), file)

    def load(self):
        try:
            file = open('record.pickle', 'rb')
        except FileNotFoundError:
            return self.get_record()
        record = pickle.load(file)
        return record


class Enemy:
    def __init__(self, approach_speed):
        self.__enemy_type = self.choose_enemy_type()
        self.__x = ENEMY_START_POS_X
        self.__y = None
        self.__width = None
        self.__height = None
        self.set_coordinates_and_size()
        self.__rect = self.make_rect()
        self.__speed = approach_speed

    def get_type(self):
        return self.__enemy_type


    @staticmethod
    def choose_enemy_type():
        random_int = random.randint(1, 2)
        if random_int == 1:
            return 'bear'
        else:
            return 'bird'

    def set_coordinates_and_size(self):
        if self.__enemy_type == 'bear':
            self.__y = BEAR_POS_Y
            self.__width = BEAR_WIDTH
            self.__height = BEAR_HEIGHT
        else:
            self.__width = BIRD_WIDTH
            self.__height = BIRD_HEIGHT
            random_int = random.randint(1, 2)
            if random_int == 1:
                self.__y = BIRD_CENTER_POS_Y
            else:
                self.__y = BIRD_TOP_POS_Y

    def make_rect(self) -> pg.Rect:
        rect = pg.Rect(self.__x, self.__y, self.__width, self.__height)
        return rect

    def get_rect(self) -> pg.Rect:
        return self.__rect

    def move(self):
        self.__rect.x -= self.__speed


class Capybara:
    def __init__(self):
        self.__x = CAPYBARA_POS_X
        self.__y = CAPYBARA_Y_POS
        self.__width = CAPYBARA_WIDTH
        self.__height = CAPYBARA_HEIGHT
        self.__gravity = GRAVITY
        self.__on_ground = True
        self.__speed_x = 8
        self.__speed_y = 0
        self.__jump_speed = -CAPYBARA_JUMP_SPEED
        self.__rect = self.make_rect()
        self.__is_falling = False

    def make_rect(self) -> pg.Rect:
        rect = pg.Rect(self.__x, self.__y, self.__width, self.__height)
        return rect

    def get_rect(self) -> pg.Rect:
        return self.__rect

    def get_speed(self):
        return round(self.__speed_x)

    def increase_speed(self):
        self.__speed_x += CAPYBARA_BONUS_SPEED

    def jump(self, need_to_jump: bool):
        if self.__on_ground is False and self.__is_falling:
            self.__speed_y += self.__gravity ** 2
            self.__rect.y += self.__speed_y

        if self.__rect.y + self.__rect.height <= 300:
            self.__is_falling = True
            self.__speed_y = 0

        if self.__rect.y + self.__rect.height > GROUND_Y_POS:
            self.__is_falling = False
            self.__on_ground = True
            self.__rect.y = CAPYBARA_Y_POS

        if self.__on_ground is False and self.__is_falling is False:
            self.__rect.y -= self.__speed_y
            if self.__speed_y > 0:
                self.__speed_y -= 1

        if need_to_jump and self.__on_ground:
            self.__on_ground = False
            self.__speed_y = CAPYBARA_BASE_SPEED

    def run(self, need_to_jump: bool):
        self.increase_speed()
        self.jump(need_to_jump)

    def respawn(self):
        self.__on_ground = True
        self.__is_falling = False
        self.__rect.y = CAPYBARA_Y_POS
        self.__speed_y = 0
