# Configuration file for MiniJam-Snakes game
# Window settings
WIDTH = 1200
HEIGHT = 800
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (44, 44, 44)
LIGHT_GRAY = (200, 200, 200)
CARD_UNSELECTED = (200, 220, 255)
CARD_SELECTED = (255, 240, 120)
LIME_GREEN = (50, 200, 50)
PASTEL_GREEN = (100, 255, 100)
FOREST_GREEN = (0, 150, 0)
CRIMSON_RED = (200, 50, 50)
LIGHT_CORAL = (255, 100, 100)
DARK_RED = (150, 0, 0)
BRIGHT_ORANGE = (255, 120, 0)
WARM_GOLDEN = (255, 180, 80)
BOLD_COBALT = (0, 100, 255)
LIGHT_SKY_BLUE = (100, 180, 255)
GRASSY_GREEN = (100, 200, 100)

# Font
MINECRAFT_FONT = "assets/fonts/minecraft.ttf"

# Grid settings (IMMUTABLE - use game_settings for runtime changes)
GRID_SIZE = 20  # Number of cells in grid (width and height)
CELL_SIZE = 25  # Size of each cell in pixels
GAP = 2         # Gap between cells in pixels

# Snake settings
SNAKE_INIT_LENGTH = 5
SNAKE_SEGMENT_SIZE = CELL_SIZE
SNAKE_GAP = GAP
INTERPOLATION_SPEED = 10.0

# Player settings (IMMUTABLE - use game_settings for runtime changes)
MAX_HAND_SIZE = 15

# Card settings
CARD_TYPES = ['Move', 'Grow', 'Shrink', 'Double Move', 'Reverse', 'Skip']
CARD_WEIGHTS = [40, 15, 15, 20, 5, 5]  # Weights for random selection
CARD_WIDTH = 80
CARD_HEIGHT = 120
CARD_GAP = 10
CARDS_PER_PAGE = 6

# Game settings (IMMUTABLE - use game_settings for runtime changes)
MAX_ROUNDS = 3
SNAKE_MOVE_INTERVAL = 0.5  # seconds between moves


class GameSettings:
    """Encapsulates mutable game settings that can be changed at runtime"""

    def __init__(self):
        # Default values from config
        self.max_rounds = MAX_ROUNDS
        self.snake_speed = SNAKE_MOVE_INTERVAL
        self.hand_size = MAX_HAND_SIZE
        self.grid_size = GRID_SIZE

    def to_dict(self):
        """Convert settings to dictionary"""
        return {
            'max_rounds': self.max_rounds,
            'snake_speed': self.snake_speed,
            'hand_size': self.hand_size,
            'grid_size': self.grid_size,
        }

    def from_dict(self, settings_dict):
        """Load settings from dictionary"""
        self.max_rounds = settings_dict.get('max_rounds', MAX_ROUNDS)
        self.snake_speed = settings_dict.get(
            'snake_speed', SNAKE_MOVE_INTERVAL)
        self.hand_size = settings_dict.get('hand_size', MAX_HAND_SIZE)
        self.grid_size = settings_dict.get('grid_size', GRID_SIZE)

    def validate(self):
        """Validate settings are within acceptable ranges"""
        self.max_rounds = max(1, min(10, int(self.max_rounds)))
        self.snake_speed = max(0.1, min(2.0, self.snake_speed))
        self.hand_size = max(5, min(20, int(self.hand_size)))
        self.grid_size = max(10, min(30, int(self.grid_size)))
