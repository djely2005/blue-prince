import pygame
from src.settings import *
class ChoiceMenu:
    def __init__(self, rect, font, choices):
        """
        choices: list of (label, callback)
        callback receives the player as parameter
        """
        self.rect = pygame.Rect(rect)
        self.font = font
        self.choices = choices
        self.other_items_rects = []
        # Do not create fonts at import time; if `font` is None, defer
        # creating a default font until draw time (after pygame.init()).

    def draw(self, screen, current_room):
        # Ensure a default font exists (creates it lazily after pygame init)
        if self.font is None:
            try:
                self.font = pygame.font.Font(None, 22)
            except Exception:
                # Fail-safe: use SysFont as fallback
                self.font = pygame.font.SysFont(None, 22)
        pygame.draw.rect(screen, (40, 40, 40), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 3)

        x = self.rect.x + 15
        y = self.rect.y + 15
        title = pygame.font.Font(None, 26).render("MENU", True, (255, 215, 0))
        screen.blit(title, (x, y))
        y += 35
        # OtherItems (consumables)
        if len(current_room.available_items):
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

        for i, (label, _) in enumerate(self.choices):
            color = (255, 255, 0) if i == self.selected_index else (200, 200, 200)
            # Draw selection highlight
            if i == self.selected_index:
                highlight_rect = pygame.Rect(x - 10, y - 2, self.rect.width - 20, 28)
                pygame.draw.rect(screen, (100, 100, 0), highlight_rect)
            text = self.font.render(label, True, color)
            screen.blit(text, (x, y))
            y += 32

    def handle_event(self, event, player):
        # Navigate menu
        if not self.choices:
            # No choices available — nothing to do
            self.selected_index = 0
            return

        if event.type == pygame.KEYDOWN:
            # Ensure selected_index is within current bounds
            n = len(self.choices)
            if self.selected_index >= n:
                self.selected_index = 0

            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % n

            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % n
            if event.key == pygame.K_RETURN:
                # Double-check index before calling
                if 0 <= self.selected_index < n:
                    _, callback = self.choices[self.selected_index]
                    callback(player)     # <<< execute chosen action
    def handle_click(self, pos: tuple) -> 'OtherItem | None':
            """Check if click is on a consumable item and return it. Otherwise return None."""
            for item_rect, item in self.other_items_rects:
                if item_rect.collidepoint(pos):
                    return item
            return None

menu = ChoiceMenu(
        rect=(MAP_WIDTH + 10, 150, INFO_WIDTH - 20, 500),
        font=None,
        choices=[]
    )