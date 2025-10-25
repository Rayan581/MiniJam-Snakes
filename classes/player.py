from .snake import Snake
from .hand import Hand
from util import Direction
from config import *
import random


class Player:
    def __init__(self, name, start_pos=(0, 0), grid_top_left=(0, 0), init_direction=Direction.RIGHT):
        self.name = name
        self.snake = Snake(start_pos, grid_top_left=grid_top_left, init_direction=init_direction)
        self.hand = Hand()

    def update(self, time_delta):
        self.snake.update(time_delta)

    def handle_events(self, event):
        self.hand.handle_events(event)

    def draw(self, surface):
        self.snake.draw(surface)
        self.hand.draw(surface)