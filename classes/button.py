import pygame
import time


class Button:
    def __init__(self, x, y, width, height, function, *,
                 text='', color=(255, 255, 255), hover_color=(150, 150, 150),
                 click_color=(100, 100, 100), border_color=(0, 0, 0),
                 border_radius=10, border_width=2, font=None, font_size=30,
                 text_color=(0, 0, 0), hover_sound=None, click_sound=None,
                 key_binding=None, tooltip_text=None, tooltip_font_size=20,
                 toggle=False, hold_time=0, initially_disabled=False, hide_when_disabled=False):

        self.rect = pygame.Rect(x, y, width, height)
        self.base_color = color
        self.color = color
        self.hover_color = hover_color
        self.click_color = click_color
        self.border_color = border_color
        self.border_radius = border_radius
        self.border_width = border_width
        self.font = pygame.font.Font(font, font_size)
        self.text_color = text_color
        self.text = text
        self.function = function
        self.hover_sound = hover_sound
        self.click_sound = click_sound
        self.key_binding = key_binding
        self.tooltip_text = tooltip_text
        self.tooltip_font = pygame.font.Font(font, tooltip_font_size)
        self.toggle = toggle
        self.is_toggled = False
        self.hold_time = hold_time
        self.hold_start_time = None
        self.disabled = initially_disabled
        self.hide_when_disabled = hide_when_disabled
        self.hovered = False
        self.clicked = False
        self.was_hovered = False

    def draw(self, screen):
        if self.hide_when_disabled and self.disabled:
            return

        # Greyed out if disabled
        display_color = (100, 100, 100) if self.disabled else self.color
        inner_rect = self.rect.inflate(-self.border_width *
                                       2, -self.border_width * 2)

        pygame.draw.rect(screen, self.border_color, self.rect,
                         border_radius=self.border_radius)
        pygame.draw.rect(screen, display_color, inner_rect,
                         border_radius=self.border_radius)

        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

        # Draw tooltip if hovered
        if self.tooltip_text and self.hovered and not self.disabled:
            tooltip_surface = self.tooltip_font.render(
                self.tooltip_text, True, (255, 255, 255))
            tooltip_rect = tooltip_surface.get_rect(
                midtop=(self.rect.centerx, self.rect.bottom + 5))
            pygame.draw.rect(screen, (0, 0, 0), tooltip_rect.inflate(10, 6))
            screen.blit(tooltip_surface, tooltip_rect)

    def update(self, events):
        if self.hide_when_disabled and self.disabled:
            return

        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

        if self.disabled:
            self.color = self.base_color
            self.clicked = False
            self.was_hovered = self.hovered
            return

        mouse_pressed = pygame.mouse.get_pressed()

        for event in events:
            if self.key_binding and event.type == pygame.KEYDOWN:
                if event.key == self.key_binding:
                    self._activate()

        if self.hovered:
            if not self.was_hovered and self.hover_sound:
                self.hover_sound.play()

            if mouse_pressed[0]:
                self.color = self.click_color
                if self.hold_time > 0:
                    if self.hold_start_time is None:
                        self.hold_start_time = time.time()
                    elif time.time() - self.hold_start_time >= self.hold_time:
                        self._activate()
                        self.hold_start_time = None
                else:
                    if not self.clicked:
                        self._activate()
                        self.clicked = True
            else:
                self.color = self.hover_color
                self.hold_start_time = None
                self.clicked = False
        else:
            self.color = self.base_color
            self.hold_start_time = None
            self.clicked = False

        self.was_hovered = self.hovered

    def _activate(self):
        if self.toggle:
            self.is_toggled = not self.is_toggled
        if self.click_sound:
            self.click_sound.play()
        self.function()

    def set_disabled(self, disabled=True):
        self.disabled = disabled
