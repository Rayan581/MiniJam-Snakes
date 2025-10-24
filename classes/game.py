import pygame
import math
import random
import os
from config import *
from .grid import Grid
from .snake import Snake


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game Template")
        self.clock = pygame.time.Clock()

        # Make the grid in the center of the window
        grid_size = 20
        cell_size = 25
        gap = 2
        grid_width = grid_size * cell_size + (grid_size - 1) * gap
        grid_height = grid_size * cell_size + (grid_size - 1) * gap
        grid_top_left = ((WIDTH - grid_width) // 2, (HEIGHT - grid_height) // 2)
        self.grid = Grid(grid_top_left, cell_size, grid_size, grid_size, color=(100, 200, 100), gap=gap)\

        snake_start_pos = (grid_size // 2, grid_size // 2)
        self.snake = Snake(snake_start_pos, segment_size=cell_size, gap=gap, init_length=5, grid_top_left=grid_top_left)

        self.running = True
        self.time = 0
        self.dt = self.clock.get_time() / 1000

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_s:
                    pass

    def update(self):
        self.dt = self.clock.get_time() / 1000
        self.time += self.dt

    def draw(self):
        self.screen.fill(DARK_GRAY)
        self.grid.draw(self.screen)
        self.snake.draw(self.screen)

        pygame.display.flip()
