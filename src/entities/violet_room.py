from src.entities.room import Room
from door import Door
from src.entities.object import Object
from src.entities.inventory import add_steps

class VioletRoom(Room):
    def __init__(self, name: str, price: int, doors: list[Door], interactables: list[Object]=[]):
        super().__init__(name, price, doors, interactables)
    
    def apply_effect(self, player):
        if self.name == "Bedroom":
            add_steps(2) # maybe player.inventory.addsteps(2) I don't know class player 
        elif self.name == "Boudoir":
            add_steps(1) # it says it can give use few extra steps (no exact amount)
    