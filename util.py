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


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
