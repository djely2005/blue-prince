# Blueprint
from src.entities.room import Room
from src.entities.door import Door
from src.entities.object import Object

class BlueRoom(Room):
    def __init__(self, name: str, price: int, doors: list[Door], interactables: list[Object]=[]):
        super().__init__(name, price, doors, interactables)