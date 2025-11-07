from src.utils.consumable_type import ConsumableType
from src.entities.object import Object
from abc import ABC

@ABC
class Event(Object):
    def __init__(self, name: str, quantity: int, field):
        super().__init__(name, quantity)
        # I don't remember what does this do
        self.__field = field

    @property
    def field(self):
        return self.__field
    @property.setter
    def field(self, field):
        self.__field = field