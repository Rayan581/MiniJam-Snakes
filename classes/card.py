import pygame

class Card:
    def __init__(self, name, direction=None, effect=None):
        self.name = name
        self.direction = direction
        self.effect = effect

    def __repr__(self):
        return f"Card(name={self.name}, direction={self.direction}, effect={self.effect})"