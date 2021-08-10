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

    