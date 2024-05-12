from abc import ABC, abstractmethod
from model.constants import DELTA_TIME
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
        print(self.value)
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


#print(rec.get_record())