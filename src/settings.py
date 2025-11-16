# settings.py

import pygame

# --- Window setup ---
WIDTH, HEIGHT = 1200, 700
MAP_RATIO = 0.55
MAP_WIDTH = int(WIDTH * MAP_RATIO)
INFO_WIDTH = WIDTH - MAP_WIDTH
GRID_HEIGHT = 9
GRID_WIDTH = 5
TILE_SIZE = 64
OFFSET_X = 20
OFFSET_Y = 20
TEXT_WIDTH = INFO_WIDTH - 20

# --- Colors ---
BLUE = (50, 100, 200)
DARK_BLUE = (20, 40, 80)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# --- Fonts ---
# Note: do NOT initialize fonts or create a display surface at import time.
# Initialize pygame and create `FONT` and `screen` inside `main()` instead.

# --- Text content ---
INFO_LINES = [
    "The Blue Prince awakens...",
    "",
    "1. Explore the castle",
    "2. Talk to the guard",
    "3. Check your inventory"
]

# screen should be created in the entrypoint after pygame.init()
