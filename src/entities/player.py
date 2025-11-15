
# src/entities/player.py
from typing import Tuple

import pygame

from src.entities.inventory import Inventory
from src.entities.map import Map  # Map is in entities/map.py


# Mapping from key labels to (row_delta, col_delta) on the grid
_DIRECTION_DELTAS: dict[str, Tuple[int, int]] = {
    "Z": (-1, 0),   # up    (AZERTY)
    "Q": (0, -1),   # left
    "S": (1,  0),   # down
    "D": (0,  1),   # right
    # also allow arrows for convenience
    "UP":    (-1, 0),
    "LEFT":  (0, -1),
    "DOWN":  (1, 0),
    "RIGHT": (0, 1),
}


class Player:
    def __init__(self, grid_position: Tuple[int, int], inventory: Inventory) -> None:
        # (row, col) on the Map grid
        self.grid_position: Tuple[int, int] = grid_position

        # Inventory containing steps, money, gems, keys, etc.
        self.__inventory: Inventory = inventory

        # Optional: last selected direction as a string ("Z","Q","UP",...)
        self.selected: str | None = None

        # Luck coefficient (can be used by room effects / items)
        self.__luck: float = 1.0

        # TEMP: selection sprite loaded directly by pygame.
        # You can replace this with a nicer system later if you want.
        self._selection_sprite = pygame.image.load("SelectionImage.png")

    # ---------- Properties ----------

    @property
    def luck(self) -> float:
        return self.__luck

    @luck.setter
    def luck(self, value: float) -> None:
        self.__luck = value

    @property
    def inventory(self) -> Inventory:
        return self.__inventory

    # ---------- Movement ----------

    def try_move_with_key(self, key_label: str, game_map: Map) -> bool:
        """
        Try to move one tile according to a key label.
        key_label: 'Z','Q','S','D' or 'UP','LEFT','DOWN','RIGHT'.

        - Asks Map.request_move(...) if the move is allowed.
        - If allowed, updates grid_position and spends 1 step.
        - Returns True if the move succeeded, False otherwise.
        """
        delta = _DIRECTION_DELTAS.get(key_label.upper())
        if not delta:
            # Invalid key, ignore the input
            return False

        r, c = self.grid_position
        target = (r + delta[0], c + delta[1])

        # In your current map.py, request_move returns a bool
        can_move = game_map.request_move(
            current_position=self.grid_position,
            future_position=target,
            player=self.inventory,  # Map will pass this to door.open_door()
        )

        if can_move:
            # Update player position and spend 1 step
            self.grid_position = target
            self.inventory.spend_steps(1)

        return can_move

    # ---------- Inventory helper methods ----------

    def add_steps(self, value: int) -> None:
        self.inventory.add_steps(value)

    def add_money(self, value: int) -> None:
        self.inventory.add_money(value)

    def add_gems(self, value: int) -> None:
        self.inventory.add_gems(value)

    def add_keys(self, value: int) -> None:
        self.inventory.add_keys(value)

    def spend_steps(self, value: int) -> None:
        self.inventory.spend_steps(value)

    def spend_money(self, value: int) -> None:
        self.inventory.spend_money(value)

    def spend_gems(self, value: int) -> None:
        self.inventory.spend_gems(value)

    def spend_keys(self, value: int) -> None:
        self.inventory.spend_keys(value)
