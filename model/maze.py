import pygame as pg
from random import choice
from model.constants import CELL_SIZE
from view.constants import MAZE_INDENTATION_X, MAZE_INDENTATION_Y, MAZE_WIDTH, MAZE_HEIGHT

pg.init()


class Cell:
    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y
        self.__walls = {
            'top': True,
            'right': True,
            'left': True,
            'bottom': True
        }
        self.__thickness = 3
        self.__is_visited = False

    def visited(self):
        self.__is_visited = True

    def is_visited(self):
        return self.__is_visited

    def remove_wall(self, wall: str):
        self.__walls[wall] = False

    def get_boundaries(self) -> list[pg.Rect]:
        boundaries = []
        x, y = self.__x * CELL_SIZE, self.__y * CELL_SIZE
        if self.__walls['top']:
            boundaries.append(pg.Rect((x + MAZE_INDENTATION_X, y + MAZE_INDENTATION_Y),
                                      (CELL_SIZE, self.__thickness)))
        if self.__walls['right']:
            boundaries.append(pg.Rect((x + CELL_SIZE + MAZE_INDENTATION_X, y + MAZE_INDENTATION_Y),
                                      (self.__thickness, CELL_SIZE)))
        if self.__walls['bottom']:
            boundaries.append(pg.Rect((x + MAZE_INDENTATION_X, y + CELL_SIZE + MAZE_INDENTATION_Y),
                                      (CELL_SIZE, self.__thickness)))
        if self.__walls['left']:
            boundaries.append(pg.Rect((x + MAZE_INDENTATION_X, y + MAZE_INDENTATION_Y),
                                      (self.__thickness, CELL_SIZE)))
        return boundaries

    def get_coordinates(self):
        return self.__x, self.__y


class Maze:
    def __init__(self):
        self.__columns = round(MAZE_WIDTH // CELL_SIZE)
        self.__rows = round(MAZE_HEIGHT // CELL_SIZE)
        self.__cells_grid = self.make_cells_grid()

    def make_cells_grid(self) -> list[Cell]:
        cells_grid = [Cell(column, row) for row in range(self.__rows) for column in range(self.__columns)]
        return cells_grid

    def check_cell(self, x: int, y: int) -> Cell | bool:
        if x < 0 or \
                x > self.__columns - 1 or \
                y < 0 or \
                y > self.__rows - 1:
            return False
        print(self.find_index(x, y))
        return self.__cells_grid[self.find_index(x, y)]

    def find_index(self, x: int, y: int):
        return x + y * self.__columns

    def check_neighbors(self, cell: Cell):
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

    def generate_maze(self) -> list[Cell]:
        current_cell = self.__cells_grid[1]
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
        return self.__cells_grid
