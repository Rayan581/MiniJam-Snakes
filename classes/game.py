import pygame
import math
import random
import os
from config import *
from .grid import Grid
from util import Direction
from .player import Player
from .card import Card
from .button import Button


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

        self.confirm_button = Button(
            x=WIDTH - 100 - 20, y=HEIGHT - 40 - 20, width=100, height=40,
            function=self.confirm_selection,
            text="Confirm",
            color=LIME_GREEN,
            hover_color=PASTEL_GREEN,
            click_color=FOREST_GREEN,
            font_size=24,
            text_color=WHITE,
            tooltip_text="Confirm Selection",
            tooltip_font_size=16,
            initially_disabled=True,
            hide_when_disabled=False
        )

        self.undo_button = Button(
            x=WIDTH - 100 - 20, y=HEIGHT - 40 - 20 - 40 - 20, width=100, height=40,
            function=self.undo_last_move,
            text="Undo",
            color=CRIMSON_RED,
            hover_color=LIGHT_CORAL,
            click_color=DARK_RED,
            font_size=24,
            text_color=WHITE,
            tooltip_text="Undo",
            tooltip_font_size=16,
            initially_disabled=False,
            hide_when_disabled=True
        )

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
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            self.players[self.turn].handle_events(event)
        self.undo_button.update(events)
        self.confirm_button.update(events)

    def update(self):
        self.dt = self.clock.get_time() / 1000
        self.time += self.dt
        self.players[self.turn].update(self.dt)

        # If no cards left in hand, enable confirm button
        if self.players[self.turn].hand_empty():
            self.confirm_button.disabled = False
        else:
            self.confirm_button.disabled = True

    def draw(self):
        self.screen.fill(DARK_GRAY)
        self.grid.draw(self.screen)
        self.players[self.turn].draw(self.screen)

        self.undo_button.draw(self.screen)
        self.confirm_button.draw(self.screen)

        pygame.display.flip()

    def undo_last_move(self):
        self.players[self.turn].undo_move()

    def confirm_selection(self):
        print(f"{self.players[self.turn].name} confirmed their selection.")
        # Switch turn to the next player
        self.turn = (self.turn + 1) % len(self.players)