# src/entities/player.py

from typing import Tuple, Optional

from src.entities.inventory import Inventory
from src.entities.map import Map


# Movement deltas for the grid
_DIRECTION_DELTAS = {
    "Z": (-1, 0),   # up
    "Q": (0, -1),   # left
    "S": (1,  0),   # down
    "D": (0,  1),   # right

    "UP":    (-1, 0),
    "LEFT":  (0, -1),
    "DOWN":  (1, 0),
    "RIGHT": (0, 1),
}


class Player:
    """
    Player on the map grid:
    - grid_position (row, col)
    - inventory (steps, money, gems, keys...)
    """

    def __init__(self, grid_position: Tuple[int, int], inventory: Inventory) -> None:
        self.grid_position: Tuple[int, int] = grid_position
        self.__inventory: Inventory = inventory

        self.selected: Optional[str] = None
        self.__luck: float = 1.0

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
        delta = _DIRECTIO`N_DELTAS.get(key_label.upper())
        if not delta:
            return False

        r, c = self.grid_position
        target = (r + delta[0], c + delta[1])

        # Map.request_move returns True/False in your version
        can_move = game_map.request_move(
            current_position=self.grid_position,
            future_position=target,
            player=self.inventory,
        )

        if can_move:
            self.grid_position = target
            self.inventory.spend_steps(1)

        return can_move

    # ---------- Inventory helpers ----------

    def add_steps(self, v): self.inventory.add_steps(v)
    def add_money(self, v): self.inventory.add_money(v)
    def add_gems(self, v): self.inventory.add_gems(v)
    def add_keys(self, v): self.inventory.add_keys(v)

    def spend_steps(self, v): self.inventory.spend_steps(v)
    def spend_money(self, v): self.inventory.spend_money(v)
    def spend_gems(self, v): self.inventory.spend_gems(v)
    def spend_keys(self, v): self.inventory.spend_keys(v)

