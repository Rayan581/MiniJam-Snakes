from .snake import Snake
from .hand import Hand
from util import Direction
from config import *
from .button import Button


class Player:
    def __init__(self, name, start_pos=(0, 0), grid_top_left=(0, 0), init_direction=Direction.RIGHT):
        self.name = name
        self.snake = Snake(start_pos, grid_top_left=grid_top_left,
                           init_direction=init_direction)
        self.hand = Hand()
        self.chosen_cards = []

        grid_width = GRID_SIZE * CELL_SIZE + (GRID_SIZE - 1) * GAP
        self.chosen_cards_draw_pos = (
            (grid_top_left[0] - CARD_WIDTH) / 2, grid_top_left[1]
        ) if name == "Player 1" else (
            grid_top_left[0] + grid_width + (
                WIDTH - (grid_top_left[0] + grid_width) - CARD_WIDTH) / 2, grid_top_left[1]
        )

    def update(self, time_delta):
        self.snake.update(time_delta)
        chosen_card = self.hand.update(chosen_card_target_pos=self.chosen_cards_draw_pos)
        if chosen_card:
            self.chosen_cards.append(chosen_card)
            self.chosen_cards_draw_pos = (
                self.chosen_cards_draw_pos[0],
                self.chosen_cards_draw_pos[1] + CARD_GAP
            )

    def handle_events(self, event):
        self.hand.handle_events(event)

    def draw(self, surface):
        self.snake.draw(surface)
        self.hand.draw(surface)
        self._draw_chosen_cards(surface)

    def _draw_chosen_cards(self, surface):
        for card in self.chosen_cards:
            card.selected = False
            card.draw(surface)

    def undo_move(self):
        if not self.chosen_cards:
            return

        print(f"Undoing move for {self.name}")
        last_card = self.chosen_cards.pop()
        self.hand.add_card(last_card)
        self.chosen_cards_draw_pos = (
            self.chosen_cards_draw_pos[0],
            self.chosen_cards_draw_pos[1] - CARD_GAP
        )

    def hand_empty(self):
        return len(self.hand.cards) == 0