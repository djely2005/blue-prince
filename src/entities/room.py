from abc import ABC, abstractmethod
from src.entities.door import Door
from src.entities.object import Object
from src.utils.rarity import Rarity
import pygame
from src.utils.direction import Direction
import random
from src.utils.assets import load_image
from src.session import Session

class Room(ABC):
    """Abstract base class for all types of rooms in Blue Prince."""

    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, session : Session, possible_items: list[Object]=[], img_path = ''):
        self.__name = name
        self.session = session
        self.__price = price
        self.__doors = doors  # list each elements has a direction and a key
        self.__rarity = rarity # 0: common / 1:standard / 2:unusual / 3:rare
        self.__possible_items = possible_items or [] # contains special objects
        self.__available_items = []
        self.__sprite = load_image(img_path)
        # rotation in 90-degree clockwise steps (0..3). This value is updated by Map when the room is rotated.
        self.__rotation = 0
        self.__visited = False
    
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
    def rarity(self):
        return self.__rarity
    @rarity.setter
    def rarity(self, rarity):
        self.__rarity = rarity

    @property
    def available_items(self):
        return self.__available_items

    @property
    def possible_item(self):
        return self.__possible_items
    @possible_item.setter
    def possible_item(self, value):
        self.__possible_items = value

    @property
    def visited(self):
        return self.__visited
    @visited.setter
    def visited(self, visited):
        self.__visited = visited

    @property
    def rotation(self):
        return self.__rotation
    @rotation.setter
    def rotation(self, rotation):
        self.__rotation = rotation
    
    @abstractmethod
    def on_enter(self, player):
        """Applies the room's special effect when the player enters."""
        pass

    @abstractmethod
    def on_draft(self, player):
        """Applies the room's special effect when the player drafts."""
        pass

    # I tried draw (with rotation)

    def draw(self, screen: pygame.Surface, pos: tuple[int, int], size: int):
        """Draw the sprite of the room with tile size. It also applies rotation sent by Map"""
        x, y = pos
        rect = pygame.Rect(x, y, size, size)

        if self.__sprite:
            scaled = pygame.transform.scale(self.__sprite, (size, size))

            # apply rotation (clockwise)
            angle = -90 * self.__rotation
            rotated = pygame.transform.rotate(scaled, angle)

            # center the rotated sprite
            rect = rotated.get_rect(center=rect.center)
            screen.blit(rotated, rect)
        else:
            pygame.draw.rect(screen, (200, 200, 200), (x, y, size, size))

        pygame.draw.rect(screen, (50, 50, 50), rect, 2) # contour?

    def door_direction_exists(self, direction: Direction) -> bool:
        """Check if this room has a door in a given direction"""
        for door in self.__doors:
            if door.direction == direction:
                return True
        return False

    def generateAvailableItems (self) ->None:
        nbPossibleItems:int =  len(self.__possible_items)
        nbAvailableItems:int = self.session.luck_radint(0,nbPossibleItems+1)
        maxRarity :int = self.__possible_items[0].rarity.value

        for i in range(1,nbPossibleItems+1):
            if(self.__possible_items[i].rarity.value > maxRarity):
                maxRarity = self.__possible_items[i].rarity.value
            

        r:int = self.session.luck_radint(0,maxRarity+1)

        while(nbAvailableItems>0):
            iterationList:list[Object] = [] 

            for item in self.__possible_items:
                if( item not in self.__possible_items and item.rarity.value >= r ):
                    iterationList.append(item)
            
            iterationListSize:int = len(iterationList) 
            
            if(iterationListSize == 0):
                maxRarity = maxRarity-1
                r = self.session.luck_radint(0,maxRarity+1)
            
            elif (iterationListSize >1):
                randomIndex:int = random.randint(0, iterationListSize-1)
                self.__available_items.append(self.__possible_items[randomIndex]) 
                nbAvailableItems = nbAvailableItems-1
            
            elif(iterationListSize == 1):
                self.__available_items.append(self.__possible_items[0]) 
                nbAvailableItems = nbAvailableItems-1

    
    def room_available_item(self, luck: float):
        """Generate one object based on the player luck"""
        self.__available_items = []
        for item in self.__possible_items:
            base_probability, item_class, init_args = item
            
            final_probability = base_probability * luck
            
            if random.random() < final_probability:
                new_item = item_class(**init_args)
                self.__available_items.append(new_item)
                break
