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
