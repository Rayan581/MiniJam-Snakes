import pygame
from config import *
from util import draw_text

class Card:
    def __init__(self, x, y, text, effect, direction=None):
        self.direction = direction
        self.effect = effect
        self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        self.text = text
        self.selected = False
        self.to_remove = False

    def __repr__(self):
        return f"Card(text={self.text.replace("\n", " ")}, effect={self.effect}, direction={self.direction}, selected={self.selected})"

    def draw(self, surface):
        color = CARD_UNSELECTED if not self.selected else CARD_SELECTED
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (50, 50, 80), self.rect, width=3, border_radius=10)

        font = pygame.font.Font(MINECRAFT_FONT, 14)
        draw_text(surface, self.text.replace(" ", "\n"), font, BLACK, self.rect.center)

    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            self.selected = True
            return True
        return False