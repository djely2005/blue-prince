from src.entities.room import Room
from door import Door
from src.entities.object import Object
from src.entities.inventory import Inventory
from src.utils.rarity import Rarity

class RedRoom(Room):
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, interactables: list[Object]=[]):
        super().__init__(name, price, doors, rarity, interactables)
    
    def apply_effect(self, player):
        if self.name == "Lavatory" :
            pass 
        elif self.name == "Gymnasium":
            Inventory.lose_steps(2)