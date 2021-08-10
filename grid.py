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
  
    def place(self, value):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(value)
            self.update_model()

            if is_valid(self.model, value, row, col) and self.solve():
                print("here")
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, value):
        row, col = self.selected
        self.cubes[row][col].set_temp(value)

    def draw(self):
        # draw grid lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.window, (0, 0, 0), (0, i*gap), (self.width, i*gap), thick) 
            pygame.draw.line(self.window, (0, 0, 0), (i*gap, 0), (i*gap, self.height), thick) 

        # draw cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.window)

    def select(self, row, col):
        for i in range(self.rows):
            for j in range (self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, position):
        if position[0] < self.width and position[1] < self.height:
            gap = self.width / 9
            x = position[0] // gap
            y = position[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

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