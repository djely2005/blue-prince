import pygame
from src.settings import *


class ChoiceMenu:
    def __init__(self, rect, font, choices):
        """
        choices: list of (label, callback)
        callback receives the player as parameter
        """
        # FIXED: rect must be the full tuple
        self.rect = pygame.Rect(rect)

        self.font = font
        self.choices = choices
        self.other_items_rects = []
        self.selected_index = 0

    def draw(self, screen, current_room):
        # Lazy-load font
        if self.font is None:
            try:
                self.font = pygame.font.Font(None, 22)
            except Exception:
                self.font = pygame.font.SysFont(None, 22)

        # ---- SHIFT THE ENTIRE MENU DOWN BY 120px ----
        draw_rect = self.rect.move(0, 120)

        # Draw background & border
        pygame.draw.rect(screen, (40, 40, 40), draw_rect)
        pygame.draw.rect(screen, (200, 200, 200), draw_rect, 3)

        # Internal margins
        x = draw_rect.x + 15
        y = draw_rect.y + 15

        # Title
        title = pygame.font.Font(None, 26).render("MENU", True, (255, 215, 0))
        screen.blit(title, (x, y))
        y += 35

        # ---- Consumables / Items available in current room ----
        if hasattr(current_room, 'available_items') and len(current_room.available_items):
            y += 8
            other_title = self.font.render("CONSUMABLES:", True, DARK_BLUE)
            screen.blit(other_title, (x, y))
            y += 32

            self.other_items_rects = []
            for item in current_room.available_items:
                item_text = self.font.render(f"- {item.name} (click to use)", True, (100, 200, 100))
                item_rect = item_text.get_rect(topleft=(x + 10, y))
                self.other_items_rects.append((item_rect, item))
                screen.blit(item_text, (x + 10, y))
                y += 32

        # ---- Menu choices ----
        for i, (label, _) in enumerate(self.choices):
            is_selected = (i == self.selected_index)
            color = (255, 255, 0) if is_selected else (200, 200, 200)

            if is_selected:
                highlight_rect = pygame.Rect(x - 10, y - 2, draw_rect.width - 20, 28)
                pygame.draw.rect(screen, (100, 100, 0), highlight_rect)

            text = self.font.render(label, True, color)
            screen.blit(text, (x, y))
            y += 32

    def handle_event(self, event, player):
        if not self.choices:
            self.selected_index = 0
            return

        if event.type == pygame.KEYDOWN:
            n = len(self.choices)

            if self.selected_index >= n:
                self.selected_index = 0

            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % n

            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % n

            if event.key == pygame.K_RETURN:
                _, callback = self.choices[self.selected_index]
                callback(player)

    def handle_click(self, pos: tuple):
        """Return clicked consumable item if any."""
        for item_rect, item in self.other_items_rects:
            if item_rect.collidepoint(pos):
                return item
        return None


# Example Creation
menu = ChoiceMenu(
    rect=(MAP_WIDTH + 10, 150, INFO_WIDTH - 20, 500),
    font=None,
    choices=[]
)
