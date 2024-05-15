import pygame as pg
from model.constants import DELTA_TIME, TIME_FOR_MAZE, CELL_SIZE
from model.classes import Timer, Record, Capybara, Enemy
from model.maze import Maze, MazePlayer, MazePrize
pg.init()


class Model:
    def __init__(self):
        self.__death_count: int = 0
        self.__timers_list: list[Timer] = []
        self.__mazes_list: list[Maze] = []
        self.__maze_players_list: list[MazePlayer] = []
        self.__maze_prize_list: list[MazePrize] = []
        self.__record: Record = Record()
        self.__pause: bool = False
        self.__enemy_stack: list[Enemy] = []
        self.__capybara: Capybara = Capybara()

    def prepare_data(self, maze_width: int,
                     maze_height: int,
                     indentation_x: int,
                     indentation_y: int):
        for death in range(1, 7):
            current_maze_number = death - 1
            cell_size = CELL_SIZE // death
            cell_indentation = cell_size // 4
            cell_size_part = cell_size // 1.25
            self.__mazes_list.append(Maze(cell_size,
                                          maze_width,
                                          maze_height,
                                          indentation_x,
                                          indentation_y))
            maze_boundaries = self.get_maze_to_render(current_maze_number)
            self.__maze_players_list.append(MazePlayer(indentation_x + cell_indentation,
                                                       indentation_y + cell_indentation,
                                                       cell_size,
                                                       death,
                                                       maze_boundaries))
            current_maze_size = self.get_maze_size(current_maze_number)
            coordinate_x_prize = current_maze_size[0] + indentation_x - cell_size_part
            coordinate_y_prize = current_maze_size[1] + indentation_y - cell_size_part
            self.__maze_prize_list.append(MazePrize(coordinate_x_prize, coordinate_y_prize, cell_size))
            time = TIME_FOR_MAZE // death
            self.__timers_list.append(Timer(time))

    def get_pause_condition(self) -> bool:
        return self.__pause

    def set_pause(self):
        self.__pause = not self.__pause

    def is_maze_time_not_over(self) -> bool:
        return self.__timers_list[self.__death_count].update()

    def get_time_for_print(self):
        return self.__timers_list[self.__death_count].get_for_print()

    def get_maze_to_render(self, maze_num: int = None) -> list[pg.Rect]:
        if maze_num is not None:
            maze = self.__mazes_list[maze_num]
        else:
            maze = self.__mazes_list[self.__death_count]
        maze_boundaries = []
        cells_list = maze.get_cells_grid()
        for cell in cells_list:
            maze_boundaries += cell.get_boundaries()
        return maze_boundaries

    def get_maze_size(self, maze_number: int = None):
        if maze_number is not None:
            maze = self.__mazes_list[maze_number]
        else:
            maze = self.__mazes_list[self.__death_count]
        return maze.get_size()

    def update_death_count(self):
        self.__death_count += 1

    def get_maze_capybara_rect(self) -> tuple[pg.Rect, bool]:
        capybara = self.__maze_players_list[self.__death_count]
        return capybara.get_rect()

    def get_prize_rect(self):
        prize = self.__maze_prize_list[self.__death_count]
        return prize.get_rect()

    def player_in_maze_move(self, buttons: list[bool]):
        player = self.__maze_players_list[self.__death_count]
        player.move(buttons)

    def is_prize_received(self) -> bool:
        player_rect = self.__maze_players_list[self.__death_count].get_rect(False)
        prize_rect = self.__maze_prize_list[self.__death_count].get_rect()
        if player_rect.colliderect(prize_rect):
            return True
        else:
            return False

    def run(self, need_to_jump: bool = False):
        if not self.__pause:
            self.__capybara.run(need_to_jump)
            self.__record.update()
            if self.get_enemy_information() is None:
                self.__enemy_stack.append(Enemy(self.get_capybara_speed()))
            else:
                enemy = self.__enemy_stack[0]
                enemy.move()
                enemy_rect = enemy.get_rect()
                if enemy_rect.right <= 0:
                    self.__enemy_stack.pop()

    def get_capybara_rect(self) -> pg.Rect:
        capybara_rect = self.__capybara.get_rect()
        return capybara_rect

    def get_capybara_state(self):
        return self.__capybara.get_state()


    def get_capybara_speed(self):
        return self.__capybara.get_speed()

    def get_enemy_information(self) -> tuple[pg.Rect, str] | None:
        if len(self.__enemy_stack) == 1:
            enemy_rect = self.__enemy_stack[0].get_rect()
            enemy_type = self.__enemy_stack[0].get_type()
            return enemy_rect, enemy_type
        else:
            return None

    def get_record_value(self) -> str:
        return self.__record.get_for_print()

    def is_capybara_dead(self) -> bool:
        capybara_rect = self.get_capybara_rect()
        enemy_rect = self.get_enemy_information()
        if enemy_rect is not None:
            if capybara_rect.colliderect(enemy_rect[0]):
                self.__death_count += 1
                self.__enemy_stack.pop()
                self.__capybara.respawn()
                return True
        else:
            return False
