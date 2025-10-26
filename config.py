# Configuration file for MiniJam-Snakes game
# Window settings
WIDTH = 800
HEIGHT = 600
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

# Grid settings
GRID_SIZE = 20  # Number of cells in grid (width and height)
CELL_SIZE = 25  # Size of each cell in pixels
GAP = 2         # Gap between cells in pixels

# Snake settings
SNAKE_INIT_LENGTH = 5
SNAKE_SEGMENT_SIZE = CELL_SIZE
SNAKE_GAP = GAP
INTERPOLATION_SPEED = 10.0

# Player settings
MAX_HAND_SIZE = 15

# Card settings
CARD_TYPES = ['Move', 'Grow', 'Shrink', 'Double Move', 'Reverse', 'Skip']
CARD_WEIGHTS = [40, 15, 15, 20, 5, 5]  # Weights for random selection
CARD_WIDTH = 80
CARD_HEIGHT = 120
CARD_GAP = 10
CARDS_PER_PAGE = 6

# Game settings
MAX_ROUNDS = 3
SNAKE_MOVE_INTERVAL = 0.5  # seconds between moves