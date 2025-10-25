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

# Grid settings
GRID_SIZE = 20  # Number of cells in grid (width and height)
CELL_SIZE = 25  # Size of each cell in pixels
GAP = 2         # Gap between cells in pixels

# Snake settings
SNAKE_INIT_LENGTH = 10
SNAKE_SEGMENT_SIZE = CELL_SIZE
SNAKE_GAP = GAP

# Movement settings
SNAKE_MOVE_INTERVAL = 0.2  # seconds between moves