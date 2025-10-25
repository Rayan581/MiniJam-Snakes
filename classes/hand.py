from .card import Card
from util import Direction
from config import *
import random
import pygame


class Hand:
    def __init__(self):
        self.cards = self._generate_random_hand()
        self.current_page = 0

    def _generate_random_hand(self):
        hand = []
        directions = list(Direction)
        effects = CARD_TYPES
        weights = CARD_WEIGHTS

        for i in range(MAX_HAND_SIZE):
            page = i // CARDS_PER_PAGE
            index_on_page = i % CARDS_PER_PAGE

            x = 100 + index_on_page * (CARD_WIDTH + CARD_GAP)
            y = HEIGHT - CARD_HEIGHT - 50

            effect = random.choices(effects, weights=weights, k=1)[0]
            name = f"{effect}"
            if effect == "Move":
                direction = random.choice(directions)
                name += "\n" + direction.name
                card = Card(x, y, name, effect, direction)
            else:
                card = Card(x, y, name, effect)
            hand.append(card)

        return hand

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            start_index = self.current_page * CARDS_PER_PAGE
            end_index = start_index + CARDS_PER_PAGE
            for card in self.cards:
                card.selected = False
            for card in self.cards[start_index:end_index]:
                if card.handle_click(pos):
                    print(f"Card clicked: {card.text.replace("\n", " ")}")
        else:
            pos = pygame.mouse.get_pos()
            start_index = self.current_page * CARDS_PER_PAGE
            end_index = start_index + CARDS_PER_PAGE
            for card in self.cards[start_index:end_index]:
                # Lift card slightly when hovered
                if card.rect.collidepoint(pos):
                    card.rect.y = HEIGHT - CARD_HEIGHT - 60
                else:
                    card.rect.y = HEIGHT - CARD_HEIGHT - 50


    def draw(self, surface):
        start_index = self.current_page * CARDS_PER_PAGE
        end_index = start_index + CARDS_PER_PAGE
        for card in self.cards[start_index:end_index]:
            card.draw(surface)