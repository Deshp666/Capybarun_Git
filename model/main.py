import pygame as pg
from model.constants import DELTA_TIME, TIME_FOR_MAZE, CELL_SIZE, JUMP_SOUND_PATH, BASIC_VOLUME
from model.time_dependent_classes import Timer, Score
from model.maze import Maze, MazePlayer, MazePrize
from model.runner_entities import Enemy, Capybara


class Model:
    def __init__(self,
                 maze_width: int,
                 maze_height: int,
                 indentation_x: int,
                 indentation_y: int):
        self.__death_count: int = 0
        self.__timers_list: list[Timer] = []
        self.__mazes_list: list[Maze] = []
        self.__maze_capybara_list: list[MazePlayer] = []
        self.__maze_prize_list: list[MazePrize] = []
        self.__score: Score = Score()
        self.__pause: bool = False
        self.__enemy_stack: list[Enemy] = []
        self.__capybara: Capybara = Capybara()
        self.__jump_sound = pg.mixer.Sound(JUMP_SOUND_PATH)
        self.__jump_sound.set_volume(BASIC_VOLUME)
        self.__sound_turned_on: bool = True
        self.__game_over = False
        self.__prepare_data(maze_width, maze_height, indentation_x, indentation_y)

    def __prepare_data(self, maze_width: int,
                       maze_height: int,
                       indentation_x: int,
                       indentation_y: int):
        for death in range(1, 40):
            current_maze_number = death - 1
            cell_size = CELL_SIZE * (0.5 + 0.5 / death)
            cell_indentation = cell_size // 4
            cell_size_part = cell_size // 1.25

            self.__mazes_list.append(Maze(cell_size,
                                          maze_width,
                                          maze_height,
                                          indentation_x,
                                          indentation_y))
            maze_boundaries = self.get_maze_to_render(current_maze_number)

            self.__maze_capybara_list.append(MazePlayer(indentation_x + cell_indentation,
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

    def toggle_pause(self):
        self.__pause = not self.__pause

    def get_sound_condition(self) -> bool:
        return self.__sound_turned_on

    def toggle_sound(self):
        if self.__sound_turned_on:
            self.__sound_turned_on = False
            self.__jump_sound.set_volume(0)
        else:
            self.__sound_turned_on = True
            self.__jump_sound.set_volume(BASIC_VOLUME)

    def play_jump_sound(self):
        if self.get_capybara_state() and not self.get_pause_condition():
            self.__jump_sound.play()

    def is_maze_time_not_over(self) -> bool:
        return self.__timers_list[self.__death_count].update()

    def get_time_for_print(self) -> str:
        return self.__timers_list[self.__death_count].get_for_print()

    def get_score(self) -> str:
        return self.__score.get_for_print()

    def get_record(self) -> str:
        return self.__score.get_record()

    def save_record(self):
        score = self.get_score()
        record = self.get_record()
        if score > record:
            self.__score.save()

    def get_maze_to_render(self, maze_num: int = None) -> list[pg.Rect]:
        if maze_num is not None:
            maze = self.__mazes_list[maze_num]
        else:
            maze = self.__mazes_list[self.__death_count]
        maze_boundaries = maze.get_boundaries()
        return maze_boundaries

    def get_maze_size(self, maze_number: int = None) -> tuple[int, int]:
        if maze_number is not None:
            maze = self.__mazes_list[maze_number]
        else:
            maze = self.__mazes_list[self.__death_count]
        return maze.get_size()

    def __update_death_count(self):
        self.__death_count += 1

    def get_maze_capybara_information(self) -> tuple[pg.Rect, bool]:
        capybara = self.__maze_capybara_list[self.__death_count]
        return capybara.get_rect()

    def get_prize_rect(self) -> pg.Rect:
        prize = self.__maze_prize_list[self.__death_count]
        return prize.get_rect()

    def capybara_in_maze_move(self, buttons: list[bool]):
        player = self.__maze_capybara_list[self.__death_count]
        player.move(buttons)

    def is_prize_received(self) -> bool:
        capybara_in_maze_rect = self.__maze_capybara_list[self.__death_count].get_rect(False)
        prize_rect = self.__maze_prize_list[self.__death_count].get_rect()
        if capybara_in_maze_rect.colliderect(prize_rect):
            if self.get_pause_condition():
                self.toggle_pause()
            return True
        else:
            return False

    def game_over(self):
        self.__game_over = True

    def run(self, need_to_jump: bool, need_to_increase_gravity: bool = False):
        if not self.__pause:
            self.__capybara.move(need_to_jump, need_to_increase_gravity)
            self.__score.update()
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

    def get_capybara_state(self) -> bool:
        return self.__capybara.is_capybara_on_ground()

    def get_capybara_speed(self) -> int:
        return self.__capybara.get_speed()

    def get_enemy_information(self) -> tuple[pg.Rect, str] | None:
        if len(self.__enemy_stack) == 1:
            enemy_rect = self.__enemy_stack[0].get_rect()
            enemy_type = self.__enemy_stack[0].get_type()
            return enemy_rect, enemy_type
        else:
            return None

    def get_record_value(self) -> str:
        return self.__score.get_for_print()

    def is_capybara_dead(self) -> bool:
        capybara_rect = self.get_capybara_rect()
        enemy_rect = self.get_enemy_information()
        if enemy_rect is not None:
            if capybara_rect.colliderect(enemy_rect[0]):
                self.__update_death_count()
                self.__enemy_stack.pop()
                self.__capybara.reset()
                return True
        else:
            return False

    def is_game_over(self) -> bool:
        return self.__game_over
