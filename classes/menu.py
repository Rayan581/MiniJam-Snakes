import pygame
from config import *
from .button import Button
from .slider import Slider
from util import draw_text


class MainMenu:
    """Main menu screen"""

    def __init__(self, screen, sound_manager):
        self.screen = screen
        self.sound_manager = sound_manager
        self.running = True
        self.next_state = None

        self.title_font = pygame.font.Font(MINECRAFT_FONT, 72)
        self.subtitle_font = pygame.font.Font(MINECRAFT_FONT, 24)

        # Button layout - now with 4 buttons
        button_width = 300
        button_height = 60
        button_x = WIDTH // 2 - button_width // 2
        start_y = HEIGHT // 2 - 90  # Adjusted to fit 4 buttons

        self.play_button = Button(
            x=button_x, y=start_y, width=button_width, height=button_height,
            function=self.start_game,
            text="Play Game",
            color=(100, 200, 100),
            hover_color=(120, 220, 120),
            click_color=(80, 180, 80),
            font=MINECRAFT_FONT,
            font_size=32,
            text_color=WHITE
        )

        self.tutorial_button = Button(
            x=button_x, y=start_y + 70, width=button_width, height=button_height,
            function=self.open_tutorial,
            text="How to Play",
            color=(255, 180, 80),  # Orange color
            hover_color=(255, 200, 100),
            click_color=(235, 160, 60),
            font=MINECRAFT_FONT,
            font_size=32,
            text_color=WHITE
        )

        self.settings_button = Button(
            x=button_x, y=start_y + 140, width=button_width, height=button_height,
            function=self.open_settings,
            text="Settings",
            color=(100, 150, 200),
            hover_color=(120, 170, 220),
            click_color=(80, 130, 180),
            font=MINECRAFT_FONT,
            font_size=32,
            text_color=WHITE
        )

        self.quit_button = Button(
            x=button_x, y=start_y + 210, width=button_width, height=button_height,
            function=self.quit_game,
            text="Quit",
            color=(200, 100, 100),
            hover_color=(220, 120, 120),
            click_color=(180, 80, 80),
            font=MINECRAFT_FONT,
            font_size=32,
            text_color=WHITE
        )

        self.buttons = [self.play_button, self.tutorial_button,
                        self.settings_button, self.quit_button]

        self.bg_offset = 0
        self.bg_speed = 20

    def start_game(self):
        self.sound_manager.play_sound('button_click')
        self.next_state = 'game'
        self.running = False

    def open_tutorial(self):
        self.sound_manager.play_sound('button_click')
        self.next_state = 'tutorial'
        self.running = False

    def open_settings(self):
        self.sound_manager.play_sound('button_click')
        self.next_state = 'settings'
        self.running = False

    def quit_game(self):
        self.sound_manager.play_sound('button_click')
        self.next_state = 'quit'
        self.running = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = 'quit'
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_state = 'quit'
                    self.running = False

        for button in self.buttons:
            old_hover = button.hovered
            button.update(events)
            if button.hovered and not old_hover:
                self.sound_manager.play_sound('button_hover')

    def update(self, dt):
        self.bg_offset += self.bg_speed * dt
        if self.bg_offset > 50:
            self.bg_offset = 0

    def draw(self):
        self.screen.fill(DARK_GRAY)

        for x in range(0, WIDTH, 50):
            for y in range(0, HEIGHT, 50):
                offset_x = int((x + self.bg_offset) % 50)
                offset_y = int((y + self.bg_offset) % 50)
                color = (60, 60, 60) if (
                    (x // 50) + (y // 50)) % 2 == 0 else (50, 50, 50)
                pygame.draw.rect(self.screen, color,
                                 (x - offset_x, y - offset_y, 50, 50))

        draw_text(self.screen, "SNAKE CARD\nBATTLE", self.title_font,
                  BRIGHT_ORANGE, (WIDTH // 2, 100), line_spacing=10)

        draw_text(self.screen, "Strategic Turn-Based Snake Combat",
                  self.subtitle_font, LIGHT_GRAY, (WIDTH // 2, 200))

        for button in self.buttons:
            button.draw(self.screen)

        pygame.display.flip()

    def run(self, clock):
        """Run the main menu loop"""
        self.sound_manager.play_music('menu', loop=True)

        while self.running:
            events = pygame.event.get()
            self.handle_events(events)

            dt = clock.tick(FPS) / 1000
            self.update(dt)
            self.draw()

        return self.next_state


class SettingsMenu:
    """Settings menu with adjustable parameters"""

    def __init__(self, screen, sound_manager, game_settings):
        self.screen = screen
        self.sound_manager = sound_manager
        self.game_settings = game_settings
        self.running = True
        self.next_state = None

        self.title_font = pygame.font.Font(MINECRAFT_FONT, 48)
        self.label_font = pygame.font.Font(MINECRAFT_FONT, 20)

        slider_x = 300
        slider_width = 200
        slider_height = 10
        start_y = 150
        spacing = 60

        self.sliders = {
            'music_volume': Slider(
                slider_x, start_y, slider_width, slider_height,
                0.0, 1.0, self.sound_manager.music_volume,
                label="Music Volume", font=MINECRAFT_FONT, font_size=20
            ),
            'sfx_volume': Slider(
                slider_x, start_y + spacing, slider_width, slider_height,
                0.0, 1.0, self.sound_manager.sfx_volume,
                label="SFX Volume", font=MINECRAFT_FONT, font_size=20
            ),
            'max_rounds': Slider(
                slider_x, start_y + spacing * 2, slider_width, slider_height,
                1, 10, self.game_settings.max_rounds,
                label="Max Rounds", font=MINECRAFT_FONT, font_size=20, force_int=True
            ),
            'snake_speed': Slider(
                slider_x, start_y + spacing * 3, slider_width, slider_height,
                0.1, 2.0, self.game_settings.snake_speed,
                label="Snake Speed", font=MINECRAFT_FONT, font_size=20
            ),
            'hand_size': Slider(
                slider_x, start_y + spacing * 4, slider_width, slider_height,
                5, 20, self.game_settings.hand_size,
                label="Hand Size", font=MINECRAFT_FONT, font_size=20, force_int=True
            ),
            'grid_size': Slider(
                slider_x, start_y + spacing * 5, slider_width, slider_height,
                10, 30, self.game_settings.grid_size,
                label="Grid Size", font=MINECRAFT_FONT, font_size=20, force_int=True
            ),
        }

        button_width = 150
        button_height = 50
        button_y = HEIGHT - 100

        self.back_button = Button(
            x=WIDTH // 2 - button_width - 10, y=button_y,
            width=button_width, height=button_height,
            function=self.go_back,
            text="Back",
            color=(200, 100, 100),
            hover_color=(220, 120, 120),
            click_color=(180, 80, 80),
            font=MINECRAFT_FONT,
            font_size=28,
            text_color=WHITE
        )

        self.apply_button = Button(
            x=WIDTH // 2 + 10, y=button_y,
            width=button_width, height=button_height,
            function=self.apply_settings,
            text="Apply",
            color=(100, 200, 100),
            hover_color=(120, 220, 120),
            click_color=(80, 180, 80),
            font=MINECRAFT_FONT,
            font_size=28,
            text_color=WHITE
        )

        self.buttons = [self.back_button, self.apply_button]

    def go_back(self):
        self.sound_manager.play_sound('button_click')
        self.next_state = 'menu'
        self.running = False

    def apply_settings(self):
        self.sound_manager.play_sound('button_click')

        self.sound_manager.set_music_volume(self.sliders['music_volume'].value)
        self.sound_manager.set_sfx_volume(self.sliders['sfx_volume'].value)

        self.game_settings.max_rounds = int(self.sliders['max_rounds'].value)
        self.game_settings.snake_speed = self.sliders['snake_speed'].value
        self.game_settings.hand_size = int(self.sliders['hand_size'].value)
        self.game_settings.grid_size = int(self.sliders['grid_size'].value)

        self.game_settings.validate()

        print("Settings applied:", self.game_settings.to_dict())

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = 'quit'
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.go_back()

        for slider in self.sliders.values():
            slider.update(events)

        for button in self.buttons:
            old_hover = button.hovered
            button.update(events)
            if button.hovered and not old_hover:
                self.sound_manager.play_sound('button_hover')

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill(DARK_GRAY)

        draw_text(self.screen, "SETTINGS", self.title_font,
                  LIGHT_GRAY, (WIDTH // 2, 80))

        for slider in self.sliders.values():
            slider.draw(self.screen)

        for button in self.buttons:
            button.draw(self.screen)

        desc_text = "Adjust game parameters. Changes apply to new games."
        draw_text(self.screen, desc_text, self.label_font,
                  (150, 150, 150), (WIDTH // 2, HEIGHT - 120))

        pygame.display.flip()

    def run(self, clock):
        """Run the settings menu loop"""
        while self.running:
            events = pygame.event.get()
            self.handle_events(events)

            dt = clock.tick(FPS) / 1000
            self.update(dt)
            self.draw()

        return self.next_state
