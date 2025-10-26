import pygame
from config import *
from classes import *

class GameManager:
    """Main game manager that handles state transitions"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Card Battle")
        self.clock = pygame.time.Clock()

        # Sound manager
        self.sound_manager = SoundManager()

        # Game settings (can be modified in settings menu)
        self.game_settings = {
            'max_rounds': MAX_ROUNDS,
            'snake_speed': SNAKE_MOVE_INTERVAL,
            'hand_size': MAX_HAND_SIZE,
            'grid_size': GRID_SIZE,
        }

        self.running = True
        self.current_state = 'menu'  # 'menu', 'game', 'settings'

    def run(self):
        """Main game loop"""
        while self.running:
            if self.current_state == 'menu':
                menu = MainMenu(self.screen, self.sound_manager)
                next_state = menu.run(self.clock)

                if next_state == 'game':
                    self.current_state = 'game'
                elif next_state == 'settings':
                    self.current_state = 'settings'
                elif next_state == 'quit':
                    self.running = False

            elif self.current_state == 'settings':
                settings = SettingsMenu(
                    self.screen, self.sound_manager, self.game_settings)
                next_state = settings.run(self.clock)

                if next_state == 'menu':
                    self.current_state = 'menu'
                elif next_state == 'quit':
                    self.running = False

            elif self.current_state == 'game':
                game = Game(self.sound_manager, self.game_settings)
                next_state = game.run(self.clock)

                if next_state == 'menu':
                    self.current_state = 'menu'
                elif next_state == 'quit':
                    self.running = False

        pygame.quit()


def main():
    game_manager = GameManager()
    game_manager.run()


if __name__ == "__main__":
    main()
