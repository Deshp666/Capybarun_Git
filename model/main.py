import pygame as pg
from model.constants import DELTA_TIME, TIME_FOR_MAZE, CELL_SIZE
from model.classes import Timer, Record
from model.maze import Maze, MazePlayer, MazePrize
pg.init()


class Model:
    def __init__(self):
        self.__speed: int = 1
        self.__death_count: int = 5
        self.__timers_list: list[Timer] = []
        self.__mazes_list: list[Maze] = []
        self.__maze_players_list: list[MazePlayer] = []
        self.__maze_prize_list: list[MazePrize] = []
        self.__record: Record = Record()
        self.__pause = False

    def prepare_data(self, maze_width: int,
                     maze_height: int,
                     indentation_x: int,
                     indentation_y: int):
        for death in range(1, 7):
            current_maze_number = death - 1
            cell_size = CELL_SIZE // death
            cell_indentetion = cell_size // 4
            cell_size_part = cell_size // 1.5
            self.__mazes_list.append(Maze(cell_size,
                                          maze_width,
                                          maze_height,
                                          indentation_x,
                                          indentation_y))
            maze_boundaries = self.get_maze_to_render(current_maze_number)
            self.__maze_players_list.append(MazePlayer(indentation_x + cell_indentetion,
                                                       indentation_y + cell_indentetion,
                                                       cell_size,
                                                       death,
                                                       maze_boundaries))
            current_maze_size = self.get_maze_size(current_maze_number)
            coordinate_x_prize = current_maze_size[0] + indentation_x - cell_size_part
            coordinate_y_prize = current_maze_size[1] + indentation_y - cell_size_part
            self.__maze_prize_list.append(MazePrize(coordinate_x_prize, coordinate_y_prize, cell_size))
            time = TIME_FOR_MAZE // death
            self.__timers_list.append(Timer(time))

    def is_maze_time_not_over(self) -> bool:
        return self.__timers_list[self.__death_count].update()

    def get_time_for_print(self):
        return self.__timers_list[self.__death_count].get_for_print()

    def get_maze_to_render(self, maze_num: int = None):
        if maze_num is not None:
            maze = self.__mazes_list[maze_num]
        else:
            maze = self.__mazes_list[self.__death_count]
        rects = []
        cells_list = maze.get_cells_grid()
        for cell in cells_list:
            rects += cell.get_boundaries()
        return rects

    def get_maze_size(self, maze_number: int = None):
        if maze_number is not None:
            maze = self.__mazes_list[maze_number]
        else:
            maze = self.__mazes_list[self.__death_count]
        return maze.get_size()

    def update_death_count(self):
        self.__death_count += 1

    def get_maze_player_rect(self) -> tuple[pg.Rect, bool]:
        player = self.__maze_players_list[self.__death_count]
        return player.get_player_rect()

    def get_prize_rect(self):
        prize = self.__maze_prize_list[self.__death_count]
        return prize.get_prize_rect()

    def player_in_maze_move(self, buttons: list[bool]):
        player = self.__maze_players_list[self.__death_count]
        player.move(buttons)

    def is_prize_received(self) -> bool:
        player_rect = self.__maze_players_list[self.__death_count].get_player_rect(False)
        prize_rect = self.__maze_prize_list[self.__death_count].get_prize_rect()
        if player_rect.colliderect(prize_rect):
            return True
        else:
            return False
