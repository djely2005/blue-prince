# settings.py

import pygame

# --- Window setup ---
WIDTH, HEIGHT = 800, 600
MAP_RATIO = 0.6
MAP_WIDTH = int(WIDTH * MAP_RATIO)
INFO_WIDTH = WIDTH - MAP_WIDTH
GRID_HEIGHT = 3 # 9
GRID_WIDTH = 3 # 5
TILE_SIZE = 64
OFFSET_X = 20
OFFSET_Y = 20
TEXT_WIDTH = 160

# --- Colors ---
BLUE = (50, 100, 200)
DARK_BLUE = (20, 40, 80)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# --- Fonts ---
pygame.font.init()
FONT = pygame.font.Font(None, 28)

# --- Text content ---
INFO_LINES = [
    "The Blue Prince awakens...",
    "",
    "1. Explore the castle",
    "2. Talk to the guard",
    "3. Check your inventory"
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
