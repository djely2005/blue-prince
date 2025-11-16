import pygame
from typing import List, Optional

from src.settings import GRAY, DARK_BLUE


class RoomSelector:
    """
    UI panel for choosing a room after opening a door.
    Displays up to 3 room cards + a Reroll button.
    """

    def __init__(self, rect: tuple, font: Optional[pygame.font.Font] = None):
        """
        Args:
            rect: (x, y, width, height) of the selector panel on the right side.
            font: Pygame Font object. If None, a default font will be created.
        """
        self.rect = pygame.Rect(rect)
        self.font = font

        self.room_choices: List = []   # list of Room instances
        self.selected_index: int = 0   # 0..len(room_choices) (last index = Reroll)
        self.active: bool = False

        self.reroll_cost: int = 1      # starts at 1, doubles each reroll
        self.reroll_requested: bool = False

    # --------------------------------------------------------------------- #
    # State management
    # --------------------------------------------------------------------- #

    def set_choices(self, room_list: List):
        """
        Activate the selector with a new set of room choices.

        Args:
            room_list: list of Room objects to choose from.
        """
        self.room_choices = list(room_list)
        self.selected_index = 0
        self.active = True
        self.reroll_cost = 1
        self.reroll_requested = False

    def clear(self):
        """Clear choices and deactivate the selector."""
        self.room_choices = []
        self.selected_index = 0
        self.active = False
        self.reroll_requested = False

    def _ensure_font(self):
        """Ensure that a usable font exists."""
        if self.font is None:
            try:
                self.font = pygame.font.Font(None, 24)
            except Exception:
                self.font = pygame.font.SysFont(None, 24)

    # --------------------------------------------------------------------- #
    # Drawing
    # --------------------------------------------------------------------- #

    def draw(self, screen: pygame.Surface, current_room=None):
        """
        Draw the room selector panel with cards and the reroll button.

        Args:
            screen: Pygame Surface to draw on.
            current_room: current room where the player is (optional, for info).
        """
        if not self.active or not self.room_choices:
            return

        self._ensure_font()
        panel = self.rect

        # Panel background
        pygame.draw.rect(screen, (240, 240, 240), panel)
        pygame.draw.rect(screen, DARK_BLUE, panel, 2)

        # Title
        title_text = "Choose a room to draft"
        title_surf = self.font.render(title_text, True, (0, 0, 0))
        screen.blit(title_surf, (panel.x + 20, panel.y + 20))

        # Current room label
        y_offset = panel.y + 50
        if current_room is not None:
            cur_text = f"Current: {getattr(current_room, 'name', 'Unknown')}"
            cur_surf = self.font.render(cur_text, True, (40, 40, 40))
            screen.blit(cur_surf, (panel.x + 20, y_offset))
            y_offset += 30
        else:
            y_offset += 10

        # Layout for cards
        padding_side = 20
        padding_between = 25

        cards_top = y_offset + 20
        reroll_area_height = 70
        cards_bottom = panel.y + panel.height - reroll_area_height - 20

        available_height = max(80, cards_bottom - cards_top)
        card_height = min(170, available_height)
        text_space = 24
        sprite_height = max(40, card_height - text_space - 16)  # leave margin + label

        num_cards = len(self.room_choices)
        if num_cards > 0:
            total_side_padding = 2 * padding_side
            total_between = padding_between * (num_cards - 1)
            card_width = (panel.width - total_side_padding - total_between) // num_cards
            card_width = max(80, min(card_width, 150))
        else:
            card_width = 120

        # Draw each card
        for idx, room in enumerate(self.room_choices):
            x = panel.x + padding_side + idx * (card_width + padding_between)
            y = cards_top
            card_rect = pygame.Rect(x, y, card_width, card_height)

            # Card background
            pygame.draw.rect(screen, (220, 220, 220), card_rect, border_radius=8)
            pygame.draw.rect(screen, (180, 180, 180), card_rect, 1, border_radius=8)

            # Room sprite
            sprite = getattr(room, "_Room__sprite", None)
            if sprite is not None:
                inner_margin = 8
                inner_w = card_width - 2 * inner_margin
                inner_h = sprite_height
                if inner_w > 0 and inner_h > 0:
                    scaled = pygame.transform.scale(sprite, (inner_w, inner_h))
                    screen.blit(scaled, (x + inner_margin, y + inner_margin))

            # Room name (centered under the sprite)
            name_surf = self.font.render(room.name, True, (0, 0, 0))
            name_rect = name_surf.get_rect(
                center=(x + card_width // 2, y + sprite_height + 8 + text_space // 2)
            )
            screen.blit(name_surf, name_rect)

            # Yellow highlight if selected
            if self.selected_index == idx:
                pygame.draw.rect(screen, (255, 230, 50), card_rect, 4, border_radius=8)

        # Reroll button area
        reroll_y = panel.y + panel.height - reroll_area_height
        reroll_rect = pygame.Rect(
            panel.x + 20, reroll_y + 15, panel.width - 40, reroll_area_height - 25
        )

        base_color = (255, 165, 0)  # orange
        border_color = base_color

        # If "Reroll" is the selected option
        if self.selected_index == len(self.room_choices):
            border_color = (255, 230, 50)  # yellow

        pygame.draw.rect(screen, (230, 230, 230), reroll_rect, border_radius=8)
        pygame.draw.rect(screen, border_color, reroll_rect, 2, border_radius=8)

        reroll_text = f"[R] Reroll - Cost: {self.reroll_cost} dice"
        reroll_surf = self.font.render(reroll_text, True, (0, 0, 0))
        rr_rect = reroll_surf.get_rect(center=reroll_rect.center)
        screen.blit(reroll_surf, rr_rect)

    # --------------------------------------------------------------------- #
    # Input handling
    # --------------------------------------------------------------------- #

    def handle_event(self, event):
        """
        Handle keyboard input for room selection.

        Returns:
            - Room instance if ENTER is pressed on a room card.
            - The string "reroll" if R or ENTER is pressed on Reroll.
            - None otherwise.
        """
        if not self.active or not self.room_choices:
            return None

        total_options = len(self.room_choices) + 1  # rooms + reroll

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_RIGHT):
                self.selected_index = (self.selected_index + 1) % total_options

            elif event.key in (pygame.K_UP, pygame.K_LEFT):
                self.selected_index = (self.selected_index - 1) % total_options

            elif event.key == pygame.K_r:
                # Direct reroll
                self.reroll_requested = True
                return "reroll"

            elif event.key == pygame.K_RETURN:
                # ENTER on a room
                if self.selected_index < len(self.room_choices):
                    selected_room = self.room_choices[self.selected_index]
                    self.clear()
                    return selected_room
                # ENTER on Reroll
                else:
                    self.reroll_requested = True
                    return "reroll"

        return None
