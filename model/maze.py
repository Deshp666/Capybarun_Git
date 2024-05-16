from random import choice
from model.constants import CAPYBARA_IN_MAZE_BASE_SPEED
import pygame as pg

pg.init()


class Cell:
    def __init__(self, x: int, y: int, size: int, indentation_x: int, indentation_y: int):
        self.__x: int = x
        self.__y: int = y
        self.__walls: dict[str: bool] = {
            'top': True,
            'right': True,
            'left': True,
            'bottom': True
        }
        self.__indentation_x: int = indentation_x
        self.__indentation_y: int = indentation_y
        self.__thickness: int = 3
        self.__size: int = size
        self.__is_visited: bool = False

    def visited(self):
        self.__is_visited = True

    def is_visited(self) -> bool:
        return self.__is_visited

    def remove_wall(self, wall: str):
        self.__walls[wall] = False

    def get_boundaries(self) -> list[pg.Rect]:
        boundaries = []
        x, y = self.__x * self.__size, self.__y * self.__size
        if self.__walls['top']:
            boundaries.append(pg.Rect((x + self.__indentation_x, y + self.__indentation_y),
                                      (self.__size, self.__thickness)))
        if self.__walls['right']:
            boundaries.append(pg.Rect((x + self.__size + self.__indentation_x, y + self.__indentation_y),
                                      (self.__thickness, self.__size)))
        if self.__walls['bottom']:
            boundaries.append(pg.Rect((x + self.__indentation_x, y + self.__size + self.__indentation_y),
                                      (self.__size, self.__thickness)))
        if self.__walls['left']:
            boundaries.append(pg.Rect((x + self.__indentation_x, y + self.__indentation_y),
                                      (self.__thickness, self.__size)))
        return boundaries

    def get_coordinates(self) -> tuple[int, int]:
        return self.__x, self.__y


class Maze:
    def __init__(self, cell_size: int,
                 maze_width: int,
                 maze_height: int,
                 indentation_x: int,
                 indentation_y: int):
        self.__cell_size: int = cell_size
        self.__indentation_x: int = indentation_x
        self.__indentation_y: int = indentation_y
        self.__columns: int = round(maze_width // self.__cell_size)
        self.__rows: int = round(maze_height // self.__cell_size)
        self.__cells_grid: list[Cell] = self.make_cells_grid()
        self.make_maze_boundaries()

    def make_cells_grid(self) -> list[Cell]:
        cells_grid = [Cell(column, row, self.__cell_size, self.__indentation_x, self.__indentation_y)
                      for row in range(self.__rows) for column in range(self.__columns)]
        return cells_grid

    def check_cell(self, x: int, y: int) -> Cell | bool:
        if x < 0 or \
                x > self.__columns - 1 or \
                y < 0 or \
                y > self.__rows - 1:
            return False
        return self.__cells_grid[self.find_index(x, y)]

    def find_index(self, x: int, y: int) -> int:
        return x + y * self.__columns

    def get_size(self) -> tuple[int, int]:
        return self.__columns * self.__cell_size, self.__rows * self.__cell_size

    def check_neighbors(self, cell: Cell) -> bool | Cell:
        neighbors = []
        x, y = cell.get_coordinates()

        top = self.check_cell(x, y - 1)
        right = self.check_cell(x + 1, y)
        bottom = self.check_cell(x, y + 1)
        left = self.check_cell(x - 1, y)

        if top and not top.is_visited():
            neighbors.append(top)
        if right and not right.is_visited():
            neighbors.append(right)
        if left and not left.is_visited():
            neighbors.append(left)
        if bottom and not bottom.is_visited():
            neighbors.append(bottom)

        if neighbors:
            return choice(neighbors)
        else:
            return False

    @staticmethod
    def remove_walls(current_cell: Cell, next_cell: Cell):
        current_cell_x, current_cell_y = current_cell.get_coordinates()
        next_cell_x, next_cell_y = next_cell.get_coordinates()
        dx = current_cell_x - next_cell_x
        dy = current_cell_y - next_cell_y

        if dx == 1:
            current_cell.remove_wall('left')
            next_cell.remove_wall('right')
        elif dx == -1:
            current_cell.remove_wall('right')
            next_cell.remove_wall('left')

        if dy == 1:
            current_cell.remove_wall('top')
            next_cell.remove_wall('bottom')
        elif dy == -1:
            current_cell.remove_wall('bottom')
            next_cell.remove_wall('top')

    def make_maze_boundaries(self):
        index = self.__columns // 2 + self.__rows // 2
        current_cell = self.__cells_grid[index]
        stack = []
        break_count = 1

        while break_count != len(self.__cells_grid):
            current_cell.visited()
            next_cell = self.check_neighbors(current_cell)

            if next_cell:
                next_cell.visited()
                break_count += 1
                stack.append(current_cell)
                self.remove_walls(current_cell, next_cell)
                current_cell = next_cell
            elif stack:
                current_cell = stack.pop()

    def get_boundaries(self) -> list[pg.Rect]:
        boundaries = []
        cells_list = self.__cells_grid
        for cell in cells_list:
            boundaries += cell.get_boundaries()
        return boundaries


class MazePlayer:
    def __init__(self, x: int, y: int, size: int, death_count: int, maze_boundaries: list[pg.Rect]):
        self.__x: int = x
        self.__y: int = y
        self.__death_count: int = death_count
        self.__speed_bonus: int = death_count // 2
        self.__speed: int = CAPYBARA_IN_MAZE_BASE_SPEED + self.__speed_bonus
        self.__width: int = size - (size // 2)
        self.__height: int = size - (size // 3)
        self.__player_rect: pg.Rect = self.make_rect()
        self.__maze_walls: list[pg.Rect] = maze_boundaries
        self.__look_right: bool = True

    def make_rect(self) -> pg.Rect:
        rect = pg.Rect(self.__x, self.__y, self.__width, self.__height)
        return rect

    def get_rect(self, need_direction: bool = True) -> tuple[pg.Rect, bool] | pg.Rect:
        if need_direction:
            return self.__player_rect, self.__look_right
        else:
            return self.__player_rect

    def move(self, buttons: list[bool]):
        if (buttons[pg.K_s] or buttons[pg.K_DOWN]) and self.can_move_down():
            self.__player_rect.y += self.__speed
        if (buttons[pg.K_w] or buttons[pg.K_UP]) and self.can_move_up():
            self.__player_rect.y -= self.__speed
        if (buttons[pg.K_a] or buttons[pg.K_LEFT]) and self.can_move_left():
            self.__player_rect.x -= self.__speed
            self.__look_right = False
        if (buttons[pg.K_d] or buttons[pg.K_RIGHT]) and self.can_move_right():
            self.__player_rect.x += self.__speed
            self.__look_right = True

    def can_move_down(self) -> bool:
        temp_rect = self.__player_rect.copy()
        temp_rect.y += self.__speed
        return temp_rect.collidelist(self.__maze_walls) == -1

    def can_move_up(self) -> bool:
        temp_rect = self.__player_rect.copy()
        temp_rect.y -= self.__speed
        return temp_rect.collidelist(self.__maze_walls) == -1

    def can_move_left(self) -> bool:
        temp_rect = self.__player_rect.copy()
        temp_rect.x -= self.__speed
        return temp_rect.collidelist(self.__maze_walls) == -1

    def can_move_right(self) -> bool:
        temp_rect = self.__player_rect.copy()
        temp_rect.x += self.__speed
        return temp_rect.collidelist(self.__maze_walls) == -1


class MazePrize:
    def __init__(self, x: int, y: int, size: int):
        self.__x: int = x
        self.__y: int = y
        self.__width: int = size - (size // 2)
        self.__height: int = size - (size // 3)
        self.__prize_rect: pg.Rect = self.make_rect()

    def make_rect(self) -> pg.Rect:
        rect = pg.Rect(self.__x, self.__y, self.__width, self.__height)
        return rect

    def get_rect(self) -> pg.Rect:
        return self.__prize_rect
