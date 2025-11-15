# main.py

import pygame
import sys
from src.settings import *
from src.entities.map import Map
from src.entities.door import Door
from src.utils.lock_state import LockState
from src.utils.direction import Direction
from src.session import session


pool = [
    {
        "name": "Antechamber",
        "price": 0,
        "doors": [
            Door(LockState.DOUBLE_LOCKED, Direction.BOTTOM),
            Door(LockState.DOUBLE_LOCKED, Direction.RIGHT),
            Door(LockState.DOUBLE_LOCKED, Direction.LEFT),
        ],
        "interactables": [],
        
    },
    {
        "name": "Antechamber",
        "price": 0,
        "doors": [
            Door(LockState.DOUBLE_LOCKED, Direction.BOTTOM),
            Door(LockState.DOUBLE_LOCKED, Direction.RIGHT),
            Door(LockState.DOUBLE_LOCKED, Direction.LEFT),
        ],
        "interactables": []
    },

]

# Change to a class HUD
def draw_info_panel(screen):
    """Draw the right-side text/info panel."""
    info_rect = pygame.Rect(MAP_WIDTH, 0, INFO_WIDTH, HEIGHT)
    pygame.draw.rect(screen, GRAY, info_rect)

    y_offset = 50
    for line in INFO_LINES:
        text_surface = FONT.render(line, True, DARK_BLUE)
        screen.blit(text_surface, (MAP_WIDTH + 20, y_offset))
        y_offset += 40


# Change to put Map class
def draw_map_area(screen):
    """Draw the left-side map area."""
    map_rect = pygame.Rect(0, 0, MAP_WIDTH, HEIGHT)
    pygame.draw.rect(screen, BLUE, map_rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Blue Prince - Prototype Display")
    clock = pygame.time.Clock()
    map = Map(0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- Draw everything ---
        screen.fill(DARK_BLUE)
        map.draw(screen)
        draw_info_panel(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
