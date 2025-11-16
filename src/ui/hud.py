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
        self.line_height = 28
        self.padding = 12

        # Transient message state
        self._message = None
        self._message_expire = 0.0

        # Click detection for consumables
        self.other_items_rects = []

    def draw(self, screen: pygame.Surface, player, room):
        """Draw the HUD panel with player inventory and stats."""

        # Ensure font exists
        if self.font is None:
            try:
                self.font = pygame.font.Font(None, 24)
            except Exception:
                self.font = pygame.font.SysFont(None, 24)

        # Background
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, DARK_BLUE, self.rect, 2)

        x = self.rect.x + self.padding
        y = self.rect.y + self.padding

        # Title
        title = self.font.render("INVENTORY", True, DARK_BLUE)
        screen.blit(title, (x, y))
        y += self.line_height + 12

        # Prepare columns
        left_x = x
        right_x = x + 180  # fixed spacing between columns

        inventory = player.inventory

        # ---- LEFT COLUMN → Permanent Items ----
        left_y = y
        if inventory.permanentItems:
            perm_title = self.font.render("PERMANENT ITEMS:", True, DARK_BLUE)
            screen.blit(perm_title, (right_x, left_y))
            left_y += self.line_height

            for item in inventory.permanentItems:
                txt = self.font.render(f"- {item.name}", True, (0, 0, 0))
                screen.blit(txt, (right_x + 10, left_y))
                left_y += self.line_height

        # ---- RIGHT COLUMN → Stats ----
        right_y = y
        stats = [
            f"Steps: {inventory.steps.quantity}",
            f"Money: {inventory.money.quantity}",
            f"Gems: {inventory.gems.quantity}",
            f"Keys: {inventory.keys.quantity}",
            f"Dice: {inventory.dice.quantity}",
        ]

        stat_title = self.font.render("STATS:", True, DARK_BLUE)
        screen.blit(stat_title, (left_x, right_y))
        right_y += self.line_height

        for stat in stats:
            txt = self.font.render(stat, True, (0, 0, 0))
            screen.blit(txt, (left_x + 10, right_y))
            right_y += self.line_height

        # Determine where to draw the next section

        # ---- Consumables under both columns ----
        if hasattr(inventory, "otherItems") and inventory.otherItems:
            other_title = self.font.render("CONSUMABLES:", True, DARK_BLUE)
            screen.blit(other_title, (x, y))
            y += self.line_height

            self.other_items_rects = []
            for item in inventory.otherItems:
                txt = self.font.render(f"- {item.name} (click to use)", True, (100, 200, 100))
                rect = txt.get_rect(topleft=(x + 10, y))
                self.other_items_rects.append((rect, item))
                screen.blit(txt, (x + 10, y))
                y += self.line_height

        # ---- Transient message ----
        if self._message and pygame.time.get_ticks() / 1000.0 < self._message_expire:
            msg_surf = self.font.render(self._message, True, (255, 255, 255))
            msg_bg = pygame.Rect(
                self.rect.x + self.padding,
                self.rect.bottom - self.line_height - self.padding - 5,
                self.rect.width - self.padding * 2,
                self.line_height + 4
            )
            pygame.draw.rect(screen, DARK_BLUE, msg_bg)
            screen.blit(msg_surf, (msg_bg.x + 4, msg_bg.y + 2))
        else:
            self._message = None

    def show_message(self, text: str, duration: float = 3.0):
        """Show a transient message on the HUD for `duration` seconds."""
        self._message = str(text)
        self._message_expire = pygame.time.get_ticks() / 1000.0 + float(duration)

    def handle_click(self, pos: tuple):
        """Return clicked consumable item if any."""
        for rect, item in self.other_items_rects:
            if rect.collidepoint(pos):
                return item
        return None
