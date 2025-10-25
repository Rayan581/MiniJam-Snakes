from .snake import Snake
from .card import Card
from util import Direction
from config import *
import random


class Player:
    def __init__(self, name, start_pos=(0, 0), grid_top_left=(0, 0), init_direction=Direction.RIGHT):
        self.name = name
        self.snake = Snake(start_pos, grid_top_left=grid_top_left, init_direction=init_direction)
        self.hand = self._generate_random_hand()

    def update(self, time_delta):
        self.snake.update(time_delta)

    def draw(self, surface):
        self.snake.draw(surface)

    def _generate_random_hand(self):
        directions = list(Direction)
        effects = CARD_TYPES
        weights = CARD_WEIGHTS
        hand = []
        for _ in range(MAX_HAND_SIZE):
            name = f"Card {_ + 1}"
            effect = random.choices(effects, weights=weights, k=1)[0]
            if effect == "Move":
                direction = random.choice(directions)
                card = Card(name, direction=direction, effect=effect)
            else:
                card = Card(name, effect=effect)
            hand.append(card)
        return hand