from abc import ABC, abstractmethod
from model.constants import DELTA_TIME, GRAVITY, CAPYBARA_BASE_SPEED_Y, CAPYBARA_JUMP_SPEED, CAPYBARA_BONUS_SPEED, \
     CAPYBARA_BASE_SPEED_X
from presenter.constants import CAPYBARA_WIDTH, CAPYBARA_HEIGHT, CAPYBARA_POS_X, CAPYBARA_Y_POS, BEAR_POS_Y,\
    ENEMY_START_POS_X, BIRD_CENTER_POS_Y, BIRD_TOP_POS_Y, GROUND_HEIGHT, BIRD_HEIGHT, BEAR_HEIGHT, BIRD_WIDTH,\
    BEAR_WIDTH, GROUND_Y_POS, BIRD_BOTTOM_POS_Y
from random import randint, choice
import pickle
import pygame as pg
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
        self.__value: int = time

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


class Score(TimeDependent):
    def __init__(self):
        self.score: int = 0
        self.record: str = self.load()

    def update(self):
        self.score += DELTA_TIME

    def get_for_print(self) -> str:
        score = self.get_score()
        score_to_print = f"{score:>04}"
        return score_to_print

    def get_score(self) -> int:
        return round(self.score)

    def get_record(self) -> str:
        return str(self.record)

    def save(self):
        with open('record.pickle', 'wb') as file:
            pickle.dump(self.get_for_print(), file)

    def load(self) -> str:
        try:
            file = open('record.pickle', 'rb')
        except FileNotFoundError:
            return self.get_for_print()
        record = pickle.load(file)
        file.close()
        return record


class Enemy:
    def __init__(self, approach_speed: int):
        self.__enemy_type: str = self.choose_enemy_type()
        self.__x: int = ENEMY_START_POS_X
        self.__y: int | None = None
        self.__width: int | None = None
        self.__height: int | None = None
        self.set_coordinates_and_size()
        self.__rect: pg.Rect = self.make_rect()
        self.__speed: int = approach_speed

    def get_type(self) -> str:
        return self.__enemy_type

    @staticmethod
    def choose_enemy_type() -> str:
        enemy_name_list = ['bear', 'bird']
        return choice(enemy_name_list)

    def set_coordinates_and_size(self):
        if self.__enemy_type == 'bear':
            self.__y = BEAR_POS_Y
            self.__width = BEAR_WIDTH
            self.__height = BEAR_HEIGHT
        else:
            self.__width = BIRD_WIDTH
            self.__height = BIRD_HEIGHT
            bird_positions = [BIRD_BOTTOM_POS_Y, BIRD_CENTER_POS_Y, BIRD_TOP_POS_Y]
            self.__y = choice(bird_positions)

    def make_rect(self) -> pg.Rect:
        rect = pg.Rect(self.__x, self.__y, self.__width, self.__height)
        return rect

    def get_rect(self) -> pg.Rect:
        return self.__rect

    def move(self):
        self.__rect.x -= self.__speed


class Capybara:
    def __init__(self):
        self.__x: int = CAPYBARA_POS_X
        self.__y: int = CAPYBARA_Y_POS
        self.__width: int = CAPYBARA_WIDTH
        self.__height: int = CAPYBARA_HEIGHT
        self.__gravity: int = GRAVITY
        self.__is_on_ground: bool = True
        self.__speed_x: float = CAPYBARA_BASE_SPEED_X
        self.__speed_y: float = 0
        self.__jump_speed: int = -CAPYBARA_JUMP_SPEED
        self.__rect: pg.Rect = self.make_rect()

    def make_rect(self) -> pg.Rect:
        rect = pg.Rect(self.__x, self.__y, self.__width, self.__height)
        return rect

    def get_rect(self) -> pg.Rect:
        return self.__rect

    def is_capybara_on_ground(self) -> bool:
        return self.__is_on_ground

    def get_speed(self) -> int:
        return round(self.__speed_x)

    def increase_speed(self):
        self.__speed_x += CAPYBARA_BONUS_SPEED

    def jump(self, need_to_jump: bool, need_to_increase_gravity: bool = False):
        if need_to_jump and self.__is_on_ground:
            self.__is_on_ground = False
            self.__speed_y = CAPYBARA_BASE_SPEED_Y

        if not self.__is_on_ground:
            self.__rect.y -= self.__speed_y
            self.__speed_y -= self.__gravity

            if need_to_increase_gravity:
                self.__speed_y -= self.__speed_x

            if self.__rect.bottom > GROUND_Y_POS:
                self.__is_on_ground = True
                self.__rect.y = CAPYBARA_Y_POS

    def run(self, need_to_jump: bool, need_to_increase_gravity: bool):
        self.increase_speed()
        self.jump(need_to_jump, need_to_increase_gravity)

    def reset(self):
        self.__is_on_ground = True
        self.__rect.y = CAPYBARA_Y_POS
        self.__speed_y = 0
