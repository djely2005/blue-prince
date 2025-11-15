from abc import ABC
from src.utils.rarity import Rarity

class Object(ABC):
    def __init__(self, name: str, quantity: int,rarity: Rarity):
        self.__name = name
        self.__rarity = rarity
        self.__quantity = quantity

    @property
    def rarity(self):
        return self.__rarity

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        self.__name = name
    
    @property
    def quantity(self):
        return self.__quantity
    
    @quantity.setter
    def quantity(self, quantity):
        self.__quantity = quantity