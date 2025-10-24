import pygame
from util import draw_rounded_rect


class Snake:
    def __init__(self, position, head_color=(200, 255, 0), body_color=(200, 200, 0), segment_size=20, gap=2, init_length=3, grid_top_left=(0, 0)):
        self.position = position  # (x, y) tuple
        self.head_color = head_color
        self.body_color = body_color
        self.segment_size = segment_size
        self.gap = gap
        # List of (x, y) tuples for each segment, index in the grid
        self.segments = [position]
        self.grid_top_left = grid_top_left

        # Initialize the snake with a given length
        for i in range(1, init_length):
            self.segments.append((position[0] - i, position[1]))

    def draw(self, surface):
        start_x, start_y = self.grid_top_left
        for i, (gx, gy) in enumerate(self.segments):
            # convert grid coords to pixel coords
            x = start_x + gx * (self.segment_size + self.gap)
            y = start_y + gy * (self.segment_size + self.gap)
            rect = (x, y, self.segment_size, self.segment_size)

            # pick color (head vs body)
            color = self.head_color if i == 0 else self.body_color

            draw_rounded_rect(surface, rect, color, radius=5)
