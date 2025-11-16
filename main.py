# main.py

import pygame
import sys
from src.settings import *
from src.entities.map import map
from src.session import session
from src.entities.choice_menu import menu


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
    pygame.display.set_caption("Blue Prince - Prototype Display")
    clock = pygame.time.Clock()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # MENU INPUT HANDLING
            menu.handle_event(event, session.player)

        # --- Draw everything ---
        screen.fill(DARK_BLUE)
        map.draw(screen)
        map.update_selected_direction(session.player, screen)
        draw_info_panel(screen)

        # Draw the right menu
        menu.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
