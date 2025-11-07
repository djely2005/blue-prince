from src.entities.object import Object
from src.utils.consumable_type import ConsumableType


class OtherItem(Object):
    def __init__(self, name: str, quantity: int, type: ConsumableType):
        super().__init__(name, quantity)
        self.__type = type
        # Check later with pygame
        self.__sprite = ""

    @property
    def type(self):
        return self.__type
    @property.setter
    def type(self, type):
        self.__type = type