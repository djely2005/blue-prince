from src.entities.room import Room
from door import Door
from src.entities.object import Object
from src.utils.rarity import Rarity

class GreenRoom(Room):
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, interactables: list[Object]=[]):
        super().__init__(name, price, doors, rarity, interactables)
    
    def apply_effect(self, player):
        if self.name == "Terrace" :
            pass
        elif self.name == "Veranda" :
            pass