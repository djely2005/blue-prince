# Blueprint
from src.entities.room import Room
from door import Door
from src.entities.object import Object
from src.entities.inventory import Inventory
from src.utils.rarity import Rarity

class BlueRoom(Room):
    def __init__(self, name: str, price: int, doors: list[Door], rarity: Rarity, interactables: list[Object]=[]):
        super().__init__(name, price, doors, rarity, interactables)
    
    def apply_effect(self, player):
        if self.name == "Nook":
            Inventory.add_keys(1)
        elif self.name == "Den":
            Inventory.add_gems(1)
        elif self.name == "Pantry":
            Inventory.add_gold(4)
        elif self.name == "Antechamber":
            print("You Win") # Maybe we can add a fon win in game to restart the game or insert a funny photo 
    
    def draft_effect(self, player):
        pass
    