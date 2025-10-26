from .snake import Snake
from .hand import Hand
from util import Direction, draw_dashed_line
from config import *
from .card_executer import CardExecuter
import pygame


class Player:
    def __init__(self, name, start_pos=(0, 0), grid_top_left=(0, 0),
                 init_direction=Direction.RIGHT, sound_manager=None,
                 max_hand_size=15, grid_size=20):
        self.name = name
        self.max_hand_size = max_hand_size
        self.grid_size = grid_size

        head_color = BRIGHT_ORANGE if name == "Player 1" else BOLD_COBALT
        body_color = WARM_GOLDEN if name == "Player 1" else LIGHT_SKY_BLUE
        self.snake = Snake(
            start_pos,
            grid_top_left=grid_top_left,
            init_direction=init_direction,
            head_color=head_color,
            body_color=body_color,
            grid_size=grid_size
        )
        self.hand = Hand(sound_manager=sound_manager,
                         max_hand_size=max_hand_size)
        self.chosen_cards = []

        self.chosen_cards_draw_pos = self._calculate_chosen_cards_pos(
            grid_top_left, grid_size)
        self.confirmed = False
        self.card_exec = None
        self.state = None

    def update(self):
        if self.confirmed:
            if self.card_exec is None:
                self.card_exec = CardExecuter(self.chosen_cards)
            self.run_simulation()
            return

        chosen_card = self.hand.update(
            chosen_card_target_pos=self.chosen_cards_draw_pos)
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
        if not self.confirmed:
            for card in self.chosen_cards:
                card.selected = False
                card.draw(surface)
        else:
            current_idx = self.card_exec.current_index
            current_card = self.chosen_cards[current_idx - 1]
            current_card.rect.y = HEIGHT // 2
            current_card.draw(surface)

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

    def _calculate_chosen_cards_pos(self, grid_top_left, grid_size):
        """Calculate position for chosen cards display"""
        grid_width = grid_size * CELL_SIZE + (grid_size - 1) * GAP

        return (
            (grid_top_left[0] - CARD_WIDTH) / 2, grid_top_left[1]
        ) if self.name == "Player 1" else (
            grid_top_left[0] + grid_width + (
                WIDTH - (grid_top_left[0] + grid_width) - CARD_WIDTH) / 2, grid_top_left[1]
        )

    def run_simulation(self):
        rounds_end = self.card_exec.update(self.snake)
        if rounds_end:
            self.state = "round_end"
            # Use max_rounds from card_exec, not hardcoded value
            self.card_exec.round = self.card_exec.max_rounds
