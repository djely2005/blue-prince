# src/entities/player.py
from typing import Tuple
from src.entities.inventory import Inventory
from src.utils.direction import Direction
from src.settings import *
import pygame
# keep long/explicit names
_DIRECTION_MAP = {
    # AZERTY
    pygame.K_z: Direction.TOP,
    pygame.K_q: Direction.LEFT,
    pygame.K_s: Direction.BOTTOM,
    pygame.K_d: Direction.RIGHT,

    # QWERTY fallback
    pygame.K_w: Direction.TOP,
    pygame.K_a: Direction.LEFT,
}

class Player:
    def __init__(self, grid_position: Tuple[int, int], inventory: Inventory) -> None:
        self.grid_position: Tuple[int, int] = grid_position
        self.__inventory: Inventory = inventory
        self.selected: Direction = None
        self.__luck: float = 1.0
        self.selection_sprite = pygame.image.load('player.png')

    @property
    def luck(self):
        return self.__luck
    
    @luck.setter
    def luck(self, value):
        self.__luck = value
    # Function was useless
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
