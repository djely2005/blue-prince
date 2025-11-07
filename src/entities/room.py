
from abc import ABC, abstractmethod
from door import Door
from src.entities.object import Object


class Room(ABC):
    """Abstract base class for all types of rooms in Blue Prince."""

    def __init__(self, name: str, price: int, doors: list[Door], interactables: list[Object]=[]):
        self.__name = name
        # maybe we can put the rarity of room with an enum
        # self.rarity = rarity # 0: common / 1:standard / 2:unusual / 3:rare
        self.__price = price
        self.__doors = doors  # list each elements has a direction and a key
        self.__interactables = interactables or [] # contains special objects like digging spots
    # Maybe we gonna add more methods like post_effect or draft_effect
    
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def price(self):
        return self.__price
    @price.setter
    def price(self, price):
        self.__price = price

    @property
    def doors(self):
        return self.__doors
    @doors.setter
    def doors(self, doors):
        self.__doors = doors

    @property
    def interactables(self):
        return self.__interactables
    @interactables.setter
    def interactables(self, interactables):
        self.__interactables = interactables

    @abstractmethod
    def apply_effect(self, player):
        """Applies the room's special effect to the player."""
        pass

    def __repr__(self):
        return f"<{self.name} (Rarity={self.rarity}, Cost={self.price})>"

