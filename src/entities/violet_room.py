from src.entities.room import Room
from door import Door
from src.entities.object import Object
from src.entities.inventory import Inventory
from src.utils.rarity import Rarity

class VioletRoom(Room):
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, interactables: list[Object]=[]):
        super().__init__(name, price, doors, rarity, interactables)
    
    def apply_effect(self, player):
        if self.name == "Bedroom":
            Inventory.add_steps(2) # I don't know class player maybe we need to connect player and inventory ?
        elif self.name == "Boudoir":
            Inventory.add_steps(1) # it says it can give use few extra steps (no exact amount)
    