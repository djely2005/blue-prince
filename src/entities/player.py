# src/entities/player.py
from typing import Tuple
from src.entities.inventory import Inventory
from src.utils.direction import Direction
import pygame

# keep long/explicit names
_DIRECTION_DELTAS = {
    "Z": (-1, 0),  # up  (AZERTY)
    "Q": (0, -1),  # left
    "S": (1,  0),  # down
    "D": (0,  1),  # right
    # also allow arrows for convenience
    "UP":    (-1, 0),
    "LEFT":  (0, -1),
    "DOWN":  (1, 0),
    "RIGHT": (0, 1),
}

class Player:
    def __init__(self, grid_position: Tuple[int, int], inventory: Inventory) -> None:
        self.grid_position: Tuple[int, int] = grid_position
        self.__inventory: Inventory = inventory
        self.selected: Direction = None
        self.__luck: float = 1.0
        self._selection_sprite = pygame.image.load(r'SelectionImage.png')
    @property
    def luck(self):
        return self.__luck
    
    @luck.setter
    def luck(self, value):
        self.__luck = value
    def try_move_with_key(self, key_label: str, game_map: MansionMap) -> MoveResult:
        """
        Ask the map if we can move. If allowed, update position and spend 1 step.
        key_label: 'Z','Q','S','D' or 'UP','LEFT','DOWN','RIGHT'.
        """
        delta = _DIRECTION_DELTAS.get(key_label.upper())
        if not delta:
            return MoveResult(False, "INVALID_KEY")

        r, c = self.grid_position
        target = (r + delta[0], c + delta[1])

        result = game_map.request_move(self.grid_position, target, self.inventory)
        if result.allowed:
            self.grid_position = target
            self.inventory.spend_steps(1)
        return result
    @property
    def inventory(self):
        return self.__inventory
    
    def add_steps(self, value):
        self.inventory.add_steps(value)
    
    def add_money(self, value):
        self.inventory.add_money(value)

    def add_gems(self, value):
        self.inventory.add_gems(value)
    
    
    def add_keys(self, value):
        self.inventory.add_keys(value)

    def spend_steps(self, value):
        self.inventory.spend_steps(value)
    
    def spend_money(self, value):
        self.inventory.spend_money(value)

    def spend_gems(self, value):
        self.inventory.spend_gems(value)
    
    
    def spend_keys(self, value):
        self.inventory.spend_keys(value)
