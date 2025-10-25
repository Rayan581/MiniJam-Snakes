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

            # reset selection
            for card in self.cards:
                card.selected = False

            # select a card with mouse
            for i, card in enumerate(self.cards[start_index:end_index]):
                if card.handle_click(pos):
                    print(f"Card chosen: {card.text.replace("\n", " ")}")
                    card.to_remove = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if (self.current_page + 1) * CARDS_PER_PAGE < len(self.cards):
                    self.current_page += 1
            elif event.key == pygame.K_LEFT:
                if self.current_page > 0:
                    self.current_page -= 1

    def update(self, chosen_card_target_pos=None):
        completed_card = None

        for card in self.cards[:]:
            if getattr(card, "to_remove", False) and chosen_card_target_pos is not None:
                target_x, target_y = chosen_card_target_pos
                # smooth movement
                card.rect.x += (target_x - card.rect.x) * 0.2
                card.rect.y += (target_y - card.rect.y) * 0.2

                # check if arrived
                if abs(card.rect.x - target_x) < 5 and abs(card.rect.y - target_y) < 5:
                    self.cards.remove(card)
                    completed_card = card
                    break  # only remove one per frame if you want

        # animate remaining cards shifting to fill gaps
        x_start = 100
        y = HEIGHT - CARD_HEIGHT - 50
        visible_cards = [
            c for c in self.cards if not getattr(c, 'to_remove', False)]
        for i, card in enumerate(visible_cards):
            target_x = x_start + (i % CARDS_PER_PAGE) * (CARD_WIDTH + CARD_GAP)
            card.rect.x += (target_x - card.rect.x) * 0.2
            card.rect.y = y

        # hover effect
        pos = pygame.mouse.get_pos()
        start_index = self.current_page * CARDS_PER_PAGE
        end_index = start_index + CARDS_PER_PAGE
        for card in self.cards[start_index:end_index]:
            if getattr(card, "to_remove", False):
                continue
            # Lift card slightly when hovered
            if card.rect.collidepoint(pos):
                card.rect.y = HEIGHT - CARD_HEIGHT - 60
            else:
                card.rect.y = HEIGHT - CARD_HEIGHT - 50

        return completed_card

    def draw(self, surface):
        start_index = self.current_page * CARDS_PER_PAGE
        end_index = start_index + CARDS_PER_PAGE
        for card in self.cards[start_index:end_index]:
            card.draw(surface)
