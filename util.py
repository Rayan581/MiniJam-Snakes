import pygame
from enum import Enum


def draw_text(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: tuple[int, int, int],
    center: tuple[int, int],
    line_spacing: int = 2
) -> None:
    """
    Draws multiline text on a Pygame surface with proper centering.

    Args:
        surface (pygame.Surface): The surface to draw the text on.
        text (str): The text to render, with '\n' for new lines.
        font (pygame.font.Font): The font object used to render text.
        color (tuple[int, int, int]): RGB color of the text.
        center (tuple[int, int]): (x, y) center position for the whole block.
        line_spacing (int): Extra vertical space (in pixels) between lines.
    """
    # Split text into lines
    lines = text.split("\n")

    # Calculate total height
    line_height = font.get_linesize()
    total_height = len(lines) * line_height + (len(lines) - 1) * line_spacing

    # Starting y coordinate (to vertically center)
    x, y = center
    start_y = y - total_height // 2

    # Draw each line
    for i, line in enumerate(lines):
        rendered = font.render(line, True, color)
        rect = rendered.get_rect(
            center=(x, start_y + i * (line_height + line_spacing) + line_height // 2))
        surface.blit(rendered, rect)


def draw_dashed_line(surface, start, end, color, dash_length=10):
    """Draw a dashed line between two points"""
    import math

    x1, y1 = start
    x2, y2 = end

    dx = x2 - x1
    dy = y2 - y1
    distance = math.sqrt(dx**2 + dy**2)

    if distance == 0:
        return

    dashes = int(distance / dash_length)

    for i in range(0, dashes, 2):  # Every other dash
        start_ratio = i / dashes
        end_ratio = min((i + 1) / dashes, 1)

        dash_start = (x1 + dx * start_ratio, y1 + dy * start_ratio)
        dash_end = (x1 + dx * end_ratio, y1 + dy * end_ratio)

        pygame.draw.line(surface, color, dash_start, dash_end, 2)


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
