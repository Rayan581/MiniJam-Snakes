import pygame
from util import draw_rounded_rect, Direction
from config import *


class Snake:
    def __init__(self, position, head_color=(200, 255, 0), body_color=(200, 200, 0), grid_top_left=(0, 0), init_direction=Direction.RIGHT):
        self.position = position  # (x, y) tuple
        self.head_color = head_color
        self.body_color = body_color
        self.segment_size = SNAKE_SEGMENT_SIZE
        self.gap = SNAKE_GAP
        self.time_since_last_move = 0

        self.direction = init_direction
        self.new_direction = [self.direction]

        # List of (x, y) tuples for each segment, index in the grid
        self.segments = [position]
        self.grid_top_left = grid_top_left

        # Initialize the snake with a given length
        for i in range(1, SNAKE_INIT_LENGTH):
            dx, dy = self.direction.value
            new_segment = (self.segments[i - 1][0] - dx,
                           self.segments[i - 1][1] - dy)
            self.segments.append(new_segment)

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

    def set_direction(self, direction):
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }

        last_direction = self.new_direction[-1] if self.new_direction else self.direction
        if direction != opposites[last_direction]:
            self.new_direction.append(direction)

    def update(self, time_delta=0):
        self.time_since_last_move += time_delta

        # Move the snake in the current direction every 0.2 seconds
        if self.time_since_last_move < SNAKE_MOVE_INTERVAL:
            return

        self.direction = self.new_direction.pop(
            0) if self.new_direction else self.direction

        dx, dy = self.direction.value
        new_head = (self.segments[0][0] + dx, self.segments[0][1] + dy)
        self.segments = [new_head] + \
            self.segments[:-1]  # move segments forward

        # Teleport snake to opposite side
        grid_width = GRID_SIZE
        grid_height = GRID_SIZE
        head_x, head_y = self.segments[0]
        head_x = head_x % grid_width
        head_y = head_y % grid_height
        self.segments[0] = (head_x, head_y)

        self.time_since_last_move = 0
