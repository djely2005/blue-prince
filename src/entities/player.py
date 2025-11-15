from typing import Tuple, Optional
import pygame

from src.entities.inventory import Inventory
from src.entities.map import Map
from src.utils.direction import Direction


# Mapping from key labels to Direction
_KEY_TO_DIRECTION = {
    "Z": Direction.TOP,
    "Q": Direction.LEFT,
    "S": Direction.BOTTOM,
    "D": Direction.RIGHT,

    "UP": Direction.TOP,
    "LEFT": Direction.LEFT,
    "DOWN": Direction.BOTTOM,
    "RIGHT": Direction.RIGHT,
}


# Direction → movement delta on the grid
_DIRECTION_DELTAS = {
    Direction.TOP:    (-1, 0),
    Direction.BOTTOM: (1, 0),
    Direction.LEFT:   (0, -1),
    Direction.RIGHT:  (0, 1),
}


class Player:
    """
    Represents the player on the map grid.

    - grid_position: (row, col) in the Map grid
    - inventory: steps, money, gems, keys, etc.
    """

    def __init__(self, grid_position: Tuple[int, int], inventory: Inventory) -> None:
        self.grid_position: Tuple[int, int] = grid_position
        self.__inventory: Inventory = inventory

        self.selected: Optional[Direction] = None
        self.__luck: float = 1.0

    # ----- Properties -----

    @property
    def luck(self) -> float:
        return self.__luck

    @luck.setter
    def luck(self, value: float) -> None:
        self.__luck = value

    @property
    def inventory(self) -> Inventory:
        return self.__inventory

    # ----- Movement -----

    def try_move_with_key(self, key_label: str, game_map: Map) -> bool:
        """
        Convert key press → Direction → movement.
        Ask Map if move allowed. If yes, update grid_position and spend 1 step.
        """
        direction = _KEY_TO_DIRECTION.get(key_label.upper())
        if not direction:
            return False

        dr, dc = _direction_delta = _DIRECTION_DELTAS[direction]
        row, col = self.grid_position
        target = (row + dr, col + dc)

        can_move = game_map.request_move(
            current_position=self.grid_position,
            future_position=target,
            player=self.inventory,   # Map uses Inventory to check locks/keys
        )

        if can_move:
            self.grid_position = target
            self.inventory.spend_steps(1)

        return can_move

    # ----- Inventory helpers -----

    def add_steps(self, value: int): self.inventory.add_steps(value)
    def add_money(self, value: int): self.inventory.add_money(value)
    def add_gems(self, value: int): self.inventory.add_gems(value)
    def add_keys(self, value: int): self.inventory.add_keys(value)

    def spend_steps(self, value: int): self.inventory.spend_steps(value)
    def spend_money(self, value: int): self.inventory.spend_money(value)
    def spend_gems(self, value: int): self.inventory.spend_gems(value)
    def spend_keys(self, value: int): self.inventory.spend_keys(value)
