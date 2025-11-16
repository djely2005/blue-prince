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

        self.font = pygame.font.SysFont(None, 28)

    def draw(self, screen):
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.choices)

            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.choices)

            if event.key == pygame.K_RETURN:
                _, callback = self.choices[self.selected_index]
                callback(player)     # <<< execute chosen action


menu = ChoiceMenu(
        rect=(MAP_WIDTH + 20, 240, TEXT_WIDTH - 40, 200),
        font=None,
        choices=[
            ("Open door", lambda player: print("OPEN DOOR action >", player.grid_position)),
            ("Check inventory", lambda player: print("MONEY >", player.inventory.money)),
            ("Wait", lambda player: print("You wait...")),
        ]
    )