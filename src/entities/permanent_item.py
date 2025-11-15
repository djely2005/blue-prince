from src.utils.consumable_type import ConsumableType
from src.entities.object import Object

class PermanentItem(Object):
    def __init__(self, name: str, quantity: int):
        super().__init__(name, quantity)