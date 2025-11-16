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
        self.selected_index = 0
        # Do not create fonts at import time; if `font` is None, defer
        # creating a default font until draw time (after pygame.init()).

    def draw(self, screen):
        # Ensure a default font exists (creates it lazily after pygame init)
        if self.font is None:
            try:
                self.font = pygame.font.Font(None, 28)
            except Exception:
                # Fail-safe: use SysFont as fallback
                self.font = pygame.font.SysFont(None, 28)
        pygame.draw.rect(screen, (40, 40, 40), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)

        x = self.rect.x + 10
        y = self.rect.y + 10

        for i, (label, _) in enumerate(self.choices):
            color = (255, 255, 0) if i == self.selected_index else (200, 200, 200)
            text = self.font.render(label, True, color)
            screen.blit(text, (x, y))
            y += 35

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


menu = ChoiceMenu(
        rect=(MAP_WIDTH + 20, 240, TEXT_WIDTH - 40, 200),
        font=None,
        choices=[]
    )