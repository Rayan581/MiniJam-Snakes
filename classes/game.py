import pygame
import math
import random
import os
from config import *
from .grid import Grid
from .snake import Snake
from util import Direction


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game Template")
        self.clock = pygame.time.Clock()

        # Make the grid in the center of the window
        grid_width = GRID_SIZE * CELL_SIZE + (GRID_SIZE - 1) * GAP
        grid_height = GRID_SIZE * CELL_SIZE + (GRID_SIZE - 1) * GAP
        grid_top_left = ((WIDTH - grid_width) // 2, (HEIGHT - grid_height) // 2)
        self.grid = Grid(grid_top_left, CELL_SIZE, GRID_SIZE, GRID_SIZE, color=(100, 200, 100), gap=GAP)\

        snake_start_pos = (GRID_SIZE // 2, GRID_SIZE // 2)
        self.snake = Snake(snake_start_pos, grid_top_left=grid_top_left)

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
                if event.key == pygame.K_w:
                    self.snake.set_direction(Direction.UP)
                elif event.key == pygame.K_s:
                    self.snake.set_direction(Direction.DOWN)
                elif event.key == pygame.K_a:
                    self.snake.set_direction(Direction.LEFT)
                elif event.key == pygame.K_d:
                    self.snake.set_direction(Direction.RIGHT)

    def update(self):
        self.dt = self.clock.get_time() / 1000
        self.time += self.dt
        self.snake.update(self.dt)

    def draw(self):
        self.screen.fill(DARK_GRAY)
        self.grid.draw(self.screen)
        self.snake.draw(self.screen)

        pygame.display.flip()
