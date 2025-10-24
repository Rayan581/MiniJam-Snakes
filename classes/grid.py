import pygame
from util import draw_rounded_rect


class Grid:
    def __init__(self, top_left, cell_size, rows, cols, color=(200, 200, 200), gap=0):
        self.top_left = top_left
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.color = color
        self.gap = gap

    def draw(self, surface):
        x0, y0 = self.top_left
        for row in range(self.rows):
            for col in range(self.cols):
                x = x0 + col * (self.cell_size + self.gap)
                y = y0 + row * (self.cell_size + self.gap)
                rect = (x, y, self.cell_size, self.cell_size)
                draw_rounded_rect(surface, rect, self.color, radius=5)
