from abc import ABC, abstractmethod
from src.entities.door import Door
from src.entities.object import Object
import pygame


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

    def __repr__(self):
        return f"<{self.name} (Cost={self.price})>"
    
    def draw(self, screen: pygame.Surface, pos: tuple[int, int], size: int):
        """
            Draw the sprite of the room
        """
        x, y = pos
        rect = pygame.Rect(x, y, size, size)

        # Base color (you can change based on rarity or price)
        pygame.draw.rect(screen, (200, 200, 200), rect)
        pygame.draw.rect(screen, (50, 50, 50), rect, 2)

        # Draw the name
        font = pygame.font.Font(None, 18)
        text = font.render(self.name, True, (0, 0, 0))
        screen.blit(text, (x + 5, y + 5))

        # Draw doors (optional)

