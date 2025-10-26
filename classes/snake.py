import pygame
from util import Direction
from config import *


class Snake:
    def __init__(self, position, head_color, body_color, grid_top_left=(0, 0),
                 init_direction=Direction.RIGHT, grid_size=20):
        self.position = position  # (x, y) tuple
        self.head_color = head_color
        self.body_color = body_color
        self.segment_size = SNAKE_SEGMENT_SIZE
        self.gap = SNAKE_GAP
        self.grid_size = grid_size

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

        # For smooth interpolation
        self.visual_segments = []  # (x, y) in pixels, not grid coords
        self.target_segments = []   # Target pixel positions
        self.interpolation_speed = INTERPOLATION_SPEED
        self._init_visual_positions()

    def _init_visual_positions(self):
        """Initialize visual positions to match current grid positions"""
        start_x, start_y = self.grid_top_left
        self.visual_segments = []
        self.target_segments = []

        for gx, gy in self.segments:
            x = start_x + gx * (self.segment_size + self.gap)
            y = start_y + gy * (self.segment_size + self.gap)
            self.visual_segments.append([x, y])
            self.target_segments.append([x, y])

    def _update_target_positions(self):
        """Update target positions based on grid positions"""
        start_x, start_y = self.grid_top_left
        self.target_segments = []

        for gx, gy in self.segments:
            x = start_x + gx * (self.segment_size + self.gap)
            y = start_y + gy * (self.segment_size + self.gap)
            self.target_segments.append([x, y])

    def update_interpolation(self, dt):
        """Smoothly interpolate visual positions towards targets"""
        # Ensure we have the right number of visual segments
        while len(self.visual_segments) < len(self.segments):
            if self.visual_segments:
                self.visual_segments.append(list(self.visual_segments[-1]))
            else:
                self._init_visual_positions()
                return

        while len(self.visual_segments) > len(self.segments):
            self.visual_segments.pop()

        # Interpolate each segment
        for i in range(len(self.visual_segments)):
            if i < len(self.target_segments):
                target_x, target_y = self.target_segments[i]
                current_x, current_y = self.visual_segments[i]

                lerp_factor = min(1.0, self.interpolation_speed * dt)
                new_x = current_x + (target_x - current_x) * lerp_factor
                new_y = current_y + (target_y - current_y) * lerp_factor

                self.visual_segments[i] = [new_x, new_y]

    def draw(self, surface, use_interpolation=True):
        """Draw snake with optional smooth interpolation"""
        if use_interpolation and self.visual_segments:
            positions = self.visual_segments
        else:
            start_x, start_y = self.grid_top_left
            positions = []
            for gx, gy in self.segments:
                x = start_x + gx * (self.segment_size + self.gap)
                y = start_y + gy * (self.segment_size + self.gap)
                positions.append([x, y])

        for i, (x, y) in enumerate(positions[::-1]):
            rect = (x, y, self.segment_size, self.segment_size)
            color = self.head_color if i == (
                len(positions) - 1) else self.body_color
            pygame.draw.rect(surface, color, rect, border_radius=5)

            if i == len(positions) - 1:
                highlight_rect = (
                    x + 2, y + 2, self.segment_size - 4, self.segment_size - 4)
                highlight_color = tuple(min(255, c + 40)
                                        for c in self.head_color)
                pygame.draw.rect(surface, highlight_color,
                                 highlight_rect, border_radius=4)

    def turn(self, turn_dir):
        if turn_dir not in ("left", "right"):
            return

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
        self.segments = [new_head] + self.segments[:-1]

        # Teleport snake to opposite side - use instance grid_size
        head_x, head_y = self.segments[0]
        head_x = head_x % self.grid_size
        head_y = head_y % self.grid_size
        self.segments[0] = (head_x, head_y)

        self._update_target_positions()

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
