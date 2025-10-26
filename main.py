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

        # Game settings (using GameSettings class instead of dict)
        self.game_settings = GameSettings()

        self.running = True
        self.current_state = 'menu'  # 'menu', 'game', 'settings', 'tutorial'

    def run(self):
        """Main game loop"""
        while self.running:
            if self.current_state == 'menu':
                # Clear any pending events before entering menu
                pygame.event.clear()

                menu = MainMenu(self.screen, self.sound_manager)
                next_state = menu.run(self.clock)

                if next_state == 'game':
                    self.current_state = 'game'
                elif next_state == 'settings':
                    self.current_state = 'settings'
                elif next_state == 'tutorial':
                    self.current_state = 'tutorial'
                elif next_state == 'quit':
                    self.running = False

            elif self.current_state == 'tutorial':
                # Clear events before tutorial
                pygame.event.clear()

                tutorial = TutorialPage(self.screen, self.sound_manager)
                next_state = tutorial.run(self.clock)

                if next_state == 'menu':
                    self.current_state = 'menu'
                elif next_state == 'quit':
                    self.running = False

            elif self.current_state == 'settings':
                # Clear events before settings
                pygame.event.clear()

                settings = SettingsMenu(
                    self.screen, self.sound_manager, self.game_settings)
                next_state = settings.run(self.clock)

                if next_state == 'menu':
                    self.current_state = 'menu'
                elif next_state == 'quit':
                    self.running = False

            elif self.current_state == 'game':
                # Clear events before game
                pygame.event.clear()

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
