# grid.py
import pygame
import random
from cube import Cube
from boards import *
from solver import *

class Grid:
    
    board = random.sample(boards, k=1)[0]

    def __init__(self, rows, cols, width, height, window):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.window = window
        self.model = None
        self.update_model()
        self.selected = None

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def solve(self):
        find = find_zero(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if is_valid(self.model, i, row, col):
                self.model[row][col] = i

                if self.solve():
                    return True

                self.model[row][col] = 0

        return False

    def solve_gui(self):
        self.update_model()
        find = find_zero(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if is_valid(self.model, i, row, col):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.window, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.window, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False