from src.entities.room import Room
from door import Door
from src.entities.object import Object
from src.utils.rarity import Rarity

class YellowRoom(Room):
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, interactables: list[Object]=[]):
        super().__init__(name, price, doors, rarity, interactables)

    def apply_effect(self, player):
        if self.name == "Commissary" :
            pass 
        elif self.name == "LaundryRoom":
            pass
    # To open the shop I think we need to do it in main