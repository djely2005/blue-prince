from src.utils.consumable_type import ConsumableType
from src.entities.object import Object


class ConsumableItem(Object):
    def __init__(self, name: str, quantity: int, type: ConsumableType):
        super().__init__(name, quantity)
        self.__type = type

    @property
    def type(self):
        return self.__type
    @type.setter
    def type(self, type):
        self.__type = type