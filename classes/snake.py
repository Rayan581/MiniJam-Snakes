import pygame
from util import Direction
from config import *


class Snake:
    def __init__(self, position, head_color=(200, 255, 0), body_color=(200, 200, 0), grid_top_left=(0, 0), init_direction=Direction.RIGHT):
        self.position = position  # (x, y) tuple
        self.head_color = head_color
        self.body_color = body_color
        self.segment_size = SNAKE_SEGMENT_SIZE
        self.gap = SNAKE_GAP

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

            pygame.draw.rect(surface, color, rect, border_radius=5)

    def turn(self, turn_dir):
        # Only 'left' or 'right' are valid
        if turn_dir not in ("left", "right"):
            return

        # Map current direction to new direction after a left or right turn
        turn_map = {
            Direction.UP:    {"left": Direction.LEFT,  "right": Direction.RIGHT},
            Direction.DOWN:  {"left": Direction.RIGHT, "right": Direction.LEFT},
            Direction.LEFT:  {"left": Direction.DOWN,  "right": Direction.UP},
            Direction.RIGHT: {"left": Direction.UP,    "right": Direction.DOWN},
        }

        last_direction = self.new_direction[-1] if self.new_direction else self.direction
        new_dir = turn_map[last_direction][turn_dir]
        self.new_direction.append(new_dir)

    def move(self):
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

    def grow(self):
        tail = self.segments[-1]
        self.segments.append(tail)

    def shrink(self):
        if len(self.segments) > 2:
            self.segments.pop()

    def reverse(self):
        self.segments.reverse()

        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }

        self.direction = opposites[self.direction]
        self.new_direction = [self.direction]
