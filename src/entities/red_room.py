from src.entities.room import Room
from door import Door
from src.entities.object import Object

class RedRoom(Room):
    def __init__(self, name: str, price: int, doors: list[Door], interactables: list[Object]=[]):
        super().__init__(name, price, doors, interactables)