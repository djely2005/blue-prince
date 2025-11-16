import pygame
from src.settings import MAP_WIDTH, INFO_WIDTH, HEIGHT, GRAY, DARK_BLUE


class RoomSelector:
    """UI for selecting a room when entering a door."""

    def __init__(self, rect: tuple, font: pygame.font.Font = None):
        """
        Initialize RoomSelector.
        
        Args:
            rect: (x, y, width, height) for the selector area
            font: pygame Font object; if None, creates default font lazily
        """
        self.rect = pygame.Rect(rect)
        self.font = font
        self.line_height = 35
        self.padding = 10
        self.room_choices = []  # List of (room, cost_string) tuples
        self.selected_index = 0
        self.active = False
        self.reroll_cost = 1  # Starts at 1, doubles each reroll
        self.reroll_requested = False  # Flag to indicate reroll was requested

    def set_choices(self, room_list):
        """
        Set the room choices to display.
        
        Args:
            room_list: List of Room objects to choose from
        """
        self.room_choices = room_list
        self.selected_index = 0
        self.active = True
        self.reroll_cost = 1  # Reset reroll cost when new choices are set
        self.reroll_requested = False

    def clear(self):
        """Clear choices and deactivate the selector."""
        self.room_choices = []
        self.selected_index = 0
        self.active = False

    def draw(self, screen: pygame.Surface, current_room=None):
        """Draw the room selector panel and show current player's room.

        Args:
            screen: pygame Surface to draw on
            current_room: optional Room instance representing where the player is
        """
        if not self.active or not self.room_choices:
            return

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
        title = self.font.render("SELECT ROOM", True, DARK_BLUE)
        screen.blit(title, (x, y))
        y += self.line_height + 2

        # Current room display
        if current_room is not None:
            cur_text = f"Current: {getattr(current_room, 'name', 'Unknown')}"
            cur_surf = self.font.render(cur_text, True, (0, 0, 0))
            screen.blit(cur_surf, (x + 6, y))
            y += self.line_height + 4
        else:
            y += self.line_height + 2

        # Draw room choices
        for i, room in enumerate(self.room_choices):
            color = (255, 255, 0) if i == self.selected_index else (0, 0, 0)
            cost_text = f"{i+1}. {room.name} (Cost: {room.price} gems)"
            text_surface = self.font.render(cost_text, True, color)
            screen.blit(text_surface, (x + 10, y))
            y += self.line_height

        # Draw reroll option
        y += 6
        reroll_color = (255, 165, 0)  # Orange for reroll
        reroll_selected = (len(self.room_choices) <= self.selected_index)
        if reroll_selected:
            reroll_color = (255, 255, 0)  # Yellow if selected

        reroll_text = f"[R] Reroll - Cost: {self.reroll_cost} dice"
        text_surface = self.font.render(reroll_text, True, reroll_color)
        screen.blit(text_surface, (x + 10, y))

    def handle_event(self, event):
        """
        Handle input for room selection.
        
        Returns:
            - Selected room if RETURN pressed
            - "reroll" string if reroll is requested
            - None otherwise
        """
        if not self.active or not self.room_choices:
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.room_choices)
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.room_choices)
            elif event.key == pygame.K_r:
                # Reroll request
                self.reroll_requested = True
                return "reroll"
            elif event.key == pygame.K_RETURN:
                selected_room = self.room_choices[self.selected_index]
                self.clear()
                return selected_room

        return None
