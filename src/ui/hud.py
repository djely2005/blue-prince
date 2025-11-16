import pygame
from src.settings import MAP_WIDTH, INFO_WIDTH, HEIGHT, GRAY, DARK_BLUE


class HUD:
    """Heads-Up Display: shows inventory and player info on the right panel."""

    def __init__(self, rect: tuple, font: pygame.font.Font = None):
        """
        Initialize HUD.
        
        Args:
            rect: (x, y, width, height) for the HUD area
            font: pygame Font object; if None, creates default font lazily
        """
        self.rect = pygame.Rect(rect)
        self.font = font
        self.line_height = 30
        self.padding = 10

    def draw(self, screen: pygame.Surface, player):
        """Draw the HUD panel with player inventory and stats."""
        # Ensure a default font exists
        if self.font is None:
            try:
                self.font = pygame.font.Font(None, 24)
            except Exception:
                self.font = pygame.font.SysFont(None, 24)

        # Draw background
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, DARK_BLUE, self.rect, 2)

        x = self.rect.x + self.padding
        y = self.rect.y + self.padding

        # Title
        title = self.font.render("INVENTORY", True, DARK_BLUE)
        screen.blit(title, (x, y))
        y += self.line_height + 5

        # Player inventory stats
        inventory = player.inventory
        stats = [
            f"Steps: {inventory.steps.quantity}",
            f"Money: {inventory.money.quantity}",
            f"Gems: {inventory.gems.quantity}",
            f"Keys: {inventory.keys.quantity}",
            f"Dice: {inventory.dice.quantity}",
        ]

        for stat in stats:
            text_surface = self.font.render(stat, True, (0, 0, 0))
            screen.blit(text_surface, (x, y))
            y += self.line_height

        # Permanent items
        if inventory.permanentItems:
            y += 10
            perm_title = self.font.render("PERMANENT ITEMS:", True, DARK_BLUE)
            screen.blit(perm_title, (x, y))
            y += self.line_height

            for item in inventory.permanentItems:
                item_text = self.font.render(f"- {item.name}", True, (0, 0, 0))
                screen.blit(item_text, (x + 10, y))
                y += self.line_height
