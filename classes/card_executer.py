from config import *


class CardExecuter:
    def __init__(self, chosen_cards):
        self.chosen_cards = chosen_cards[:]
        self.current_index = 0
        self.round = 1
        self.max_rounds = MAX_ROUNDS
        self.finished = False

    def update(self, snake):
        if self.finished:
            return None

        if self.current_index < len(self.chosen_cards):
            current_card = self.chosen_cards[self.current_index]

            # Execute the current card
            result = current_card.execute(snake)

            if result in ("win", "lose", "draw"):
                self.finished = True
                return result

            self.current_index += 1

        else:
            self.current_index = 0
            self.round += 1
            if self.round > self.max_rounds:
                self.finished = True
                return "draw"

        return None
