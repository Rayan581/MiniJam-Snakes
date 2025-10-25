import pygame
import math
import random
import os
from config import *
from .grid import Grid
from util import Direction
from .player import Player
from .card import Card


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

        player_one_start = (SNAKE_INIT_LENGTH, 0) # Top-left corner
        player_one = Player("Player 1", start_pos=player_one_start, grid_top_left=grid_top_left, init_direction=Direction.RIGHT)
        player_two_start = (GRID_SIZE - SNAKE_INIT_LENGTH - 1, GRID_SIZE - 1) # Bottom-right corner
        player_two = Player("Player 2", start_pos=player_two_start, grid_top_left=grid_top_left, init_direction=Direction.LEFT)
        self.players = [player_one, player_two]

        self.turn = 0  # Index of current player's turn

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
            self.players[self.turn].handle_events(event)

    def update(self):
        self.dt = self.clock.get_time() / 1000
        self.time += self.dt
        self.players[self.turn].update(self.dt)

    def draw(self):
        self.screen.fill(DARK_GRAY)
        self.grid.draw(self.screen)
        self.players[self.turn].draw(self.screen)

        pygame.display.flip()
