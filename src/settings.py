# settings.py

import pygame

# --- Window setup ---
WIDTH, HEIGHT = 800, 600
MAP_RATIO = 0.6
MAP_WIDTH = int(WIDTH * MAP_RATIO)
INFO_WIDTH = WIDTH - MAP_WIDTH

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
