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
        self.room_choices = []      # List[Room]
        self.selected_index = 0     # 0..len(rooms) for reroll
        self.active = False
        self.reroll_cost = 1        # starts at 1, doubles each reroll
        self.reroll_requested = False

    def set_choices(self, room_list):
        """
        Set the room choices to display.
        
        Args:
            room_list: List of Room objects to choose from
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
        if self.font is None:
            try:
                self.font = pygame.font.Font(None, 24)
            except Exception:
                self.font = pygame.font.SysFont(None, 24)

    def draw(self, screen: pygame.Surface, current_room=None):
        """
        Draw the room selector panel with 3 cards (like the example).
        """
        if not self.active or not self.room_choices:
            return

        self._ensure_font()

        panel = self.rect

        # Fond du panneau
        pygame.draw.rect(screen, (240, 240, 240), panel)
        pygame.draw.rect(screen, DARK_BLUE, panel, 2)

        # Titre
        title_text = "Choose a room to draft"
        title_surf = self.font.render(title_text, True, (0, 0, 0))
        screen.blit(title_surf, (panel.x + 20, panel.y + 20))

        # Affichage de la room actuelle (optionnel)
        y_offset = panel.y + 50
        if current_room is not None:
            cur_text = f"Current: {getattr(current_room, 'name', 'Unknown')}"
            cur_surf = self.font.render(cur_text, True, (40, 40, 40))
            screen.blit(cur_surf, (panel.x + 20, y_offset))
            y_offset += 30
        else:
            y_offset += 10

        # Zone centrale pour les cartes
        cards_top = y_offset + 20
        cards_height = panel.height // 2
        padding = 20
        nb_cards = len(self.room_choices)

        # largeur adaptée au panneau
        if nb_cards > 0:
            total_padding = padding * (nb_cards + 1)
            card_width = (panel.width - total_padding)
            if nb_cards > 0:
                card_width //= nb_cards
            card_width = max(80, min(card_width, 150))
        else:
            card_width = 120

        card_height = min(150, cards_height)

        # Dessiner les cartes des rooms
        for idx, room in enumerate(self.room_choices):
            x = panel.x + padding + idx * (card_width + padding)
            y = cards_top

            card_rect = pygame.Rect(x, y, card_width, card_height)

            # Fond de la carte
            pygame.draw.rect(screen, (220, 220, 220), card_rect, border_radius=8)
            pygame.draw.rect(screen, (180, 180, 180), card_rect, 1, border_radius=8)

            # Sprite de la room si dispo
            sprite = getattr(room, "_Room__sprite", None)
            if sprite is not None:
                # on garde un peu de marge à l'intérieur de la carte
                inner_margin = 8
                inner_w = card_width - 2 * inner_margin
                inner_h = card_height - 2 * inner_margin - 30  # laisser de la place pour le texte
                if inner_w > 0 and inner_h > 0:
                    scaled = pygame.transform.scale(sprite, (inner_w, inner_h))
                    screen.blit(scaled, (x + inner_margin, y + inner_margin))

            # Nom de la room sous le sprite
            name_surf = self.font.render(room.name, True, (0, 0, 0))
            name_rect = name_surf.get_rect(center=(x + card_width // 2, y + card_height - 15))
            screen.blit(name_surf, name_rect)

            # Bordure jaune si sélectionnée
            if self.selected_index == idx:
                pygame.draw.rect(screen, (255, 230, 50), card_rect, 4, border_radius=8)

        # Bouton Reroll en bas
        reroll_y = panel.y + panel.height - 60
        reroll_rect = pygame.Rect(panel.x + 20, reroll_y, panel.width - 40, 40)
        base_color = (255, 165, 0)
        border_color = base_color

        # Si le reroll est sélectionné
        if self.selected_index == len(self.room_choices):
            border_color = (255, 230, 50)

        pygame.draw.rect(screen, (230, 230, 230), reroll_rect, border_radius=8)
        pygame.draw.rect(screen, border_color, reroll_rect, 2, border_radius=8)

        reroll_text = f"[R] Reroll - Cost: {self.reroll_cost} dice"
        reroll_surf = self.font.render(reroll_text, True, (0, 0, 0))
        rr_rect = reroll_surf.get_rect(center=reroll_rect.center)
        screen.blit(reroll_surf, rr_rect)

    def handle_event(self, event):
        """
        Handle input for room selection.
        
        Returns:
            - Selected room if RETURN pressed on a room
            - "reroll" string if reroll is selected (ENTER or 'R')
            - None otherwise
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
                # Reroll direct
                self.reroll_requested = True
                return "reroll"

            elif event.key == pygame.K_RETURN:
                # ENTER sur une room
                if self.selected_index < len(self.room_choices):
                    selected_room = self.room_choices[self.selected_index]
                    self.clear()
                    return selected_room
                else:
                    # ENTER sur Reroll
                    self.reroll_requested = True
                    return "reroll"

        return None
