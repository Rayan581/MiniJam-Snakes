import pygame
from util import draw_text


class Slider:
    """Slider UI element for settings"""

    def __init__(self, x, y, width, height, min_val, max_val, initial_val,
                 label="", font=None, font_size=20, force_int=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.force_int = force_int
        self.font = pygame.font.Font(
            font, font_size) if font else pygame.font.Font(None, font_size)

        self.dragging = False
        self.handle_radius = height // 2 + 2

        # Colors
        self.track_color = (100, 100, 100)
        self.fill_color = (100, 200, 100)
        self.handle_color = (255, 255, 255)
        self.handle_hover_color = (200, 200, 200)

    def get_handle_x(self):
        """Calculate handle x position based on current value"""
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        return self.rect.x + int(ratio * self.rect.width)

    def update(self, events):
        """Update slider state"""
        mouse_pos = pygame.mouse.get_pos()
        handle_x = self.get_handle_x()
        handle_rect = pygame.Rect(handle_x - self.handle_radius,
                                  self.rect.centery - self.handle_radius,
                                  self.handle_radius * 2, self.handle_radius * 2)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if handle_rect.collidepoint(mouse_pos) or self.rect.collidepoint(mouse_pos):
                    self.dragging = True
                    self._update_value_from_mouse(mouse_pos[0])
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.dragging = False
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                self._update_value_from_mouse(mouse_pos[0])

    def _update_value_from_mouse(self, mouse_x):
        """Update value based on mouse position"""
        ratio = (mouse_x - self.rect.x) / self.rect.width
        ratio = max(0, min(1, ratio))
        val = self.min_val + ratio * (self.max_val - self.min_val)

        # Snap to integer if needed
        if self.force_int or isinstance(self.min_val, int) and isinstance(self.max_val, int):
            val = int(round(val))

        self.value = val

    def draw(self, surface):
        """Draw the slider"""
        # Draw track
        pygame.draw.rect(surface, self.track_color, self.rect,
                         border_radius=self.rect.height // 2)

        # Draw filled portion
        handle_x = self.get_handle_x()
        fill_rect = pygame.Rect(self.rect.x, self.rect.y,
                                handle_x - self.rect.x, self.rect.height)
        pygame.draw.rect(surface, self.fill_color, fill_rect,
                         border_radius=self.rect.height // 2)

        # Draw handle
        mouse_pos = pygame.mouse.get_pos()
        handle_rect = pygame.Rect(handle_x - self.handle_radius,
                                  self.rect.centery - self.handle_radius,
                                  self.handle_radius * 2, self.handle_radius * 2)

        handle_color = self.handle_hover_color if handle_rect.collidepoint(
            mouse_pos) else self.handle_color
        pygame.draw.circle(surface, handle_color, (handle_x,
                           self.rect.centery), self.handle_radius)
        pygame.draw.circle(surface, (50, 50, 50), (handle_x,
                           self.rect.centery), self.handle_radius, width=2)

        # Draw label
        if self.label:
            label_surface = self.font.render(self.label, True, (255, 255, 255))
            label_rect = label_surface.get_rect(
                midright=(self.rect.x - 20, self.rect.centery))
            surface.blit(label_surface, label_rect)

        # Draw value
        if isinstance(self.value, float):
            value_text = f"{self.value:.2f}"
        else:
            value_text = str(int(self.value))
        value_surface = self.font.render(value_text, True, (255, 255, 255))
        value_rect = value_surface.get_rect(
            midleft=(self.rect.right + 20, self.rect.centery))
        surface.blit(value_surface, value_rect)
