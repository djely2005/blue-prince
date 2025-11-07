from src.entities.room import Room
from door import Door
from src.entities.object import Object

class YellowRoom(Room):
    def __init__(self,name: str, price: int, doors: list[Door], interactables: list[Object]=[]):
        super().__init__(name, price, doors, interactables)

    def apply_effect(self, player):
        if self.name == "Commissary" :
            pass 
        elif self.name == "LaundryRoom":
            pass